import _sqlite3
import csv
import os
import os.path
import re
from os import listdir
from os.path import isfile, join

import pandas as pd

import db.queries.insertions as q
from db import ads_data_path
from db import categories_path
from db import db_path
from db import search_queries_data_path
from db.data import col
from db.data import drop_list
from db.data import parsed_data_path
from db.data import raw_data_path


def parse_categories(path):
    """
    Reads all the categories from categories.csv file and inserts them
    into categories table in database specified by path.

    :param path: The path to the database
    :type path: str

    """

    conn = _sqlite3.connect(db_path + path)
    cursor = conn.cursor()
    with open(categories_path) as infile:
        reader = csv.reader(infile)
        first_line = True
        for category in reader:
            if first_line:
                first_line = False
                continue
            print(category)
            record = [category[0], category[2], category[1]]
            q.categories_insert(cursor, tuple(record))
    conn.commit()


def replace_f_t(x):
    """
    Replaces strings f and t into binary equivalents 1 and 0.

    :param x: The string to replace.
    :return: The replaced string.
    """
    if x == "f":
        return "0"
    elif x == "t":
        return "1"
    else:
        return x


def parse_ads(db_name):
    """
    Parses ads from 001_anonimized file for given month and inserts them into
    database. File and database are specified by db_name
    The full path is created by joining the db.db_path with db_name

    :param db_name: The name to the database
    :type db_name: str

    """

    conn = _sqlite3.connect(db_path + db_name)
    cursor = conn.cursor()

    db_name = ads_data_path.replace('#', db_name)
    with open(db_name) as infile:
        # Read whole file at once
        file_string = infile.read()

        # Entry columns are separated by ","
        # Entries are separated by "\n"\

        # Sometimes, there will be "","" used in product description, e.g "Movie Title 2"
        # do not split on such cases
        all_columns = re.split('(?<![0-9a-zA-Z?! ]\")\",\"(?!\"[0-9a-zA-Z])|(?<!\n)\"\n\"(?!\")', file_string)

        entry = []
        column_counter = 0
        entry_counter = 0

        for column in all_columns:
            # There are 29 columns in entry
            if column_counter == 29:
                # Sometimes there are leftover " in first column
                # get rid of them
                entry[0] = entry[0].strip('"')

                # DEBUG - if there are any illegal chars in user product description
                # it prints where they are so that we can fix/remove them
                print(entry)

                # if is_date(entry[10]) and is_zero_or_one(entry[14]):
                #    print("OK!")

                entries = map(replace_f_t, entry)
                # Add the entry to the db
                # WARNING - unfiltered tuple input, assuming that
                # none of the OLX users is named DROP TABLE ADS
                if entry_counter != 0:
                    q.ads_insert(cursor, tuple(entries))

                entry = []
                column_counter = 0

                entry_counter += 1

            entry.append(column)
            column_counter += 1
        conn.commit()
    return


def drop_columns(entry, drop):
    dropped_count = 1
    for column in drop:
        del entry[column - dropped_count]
        dropped_count += 1
    return entry


def parse_ads_to_csv(filename):
    """
       Parses ads db_file and writes it to csv.
       :param filename: The path file containing all the months data
       :type filename: str
    """

    with open(raw_data_path + filename) as infile:
        # Read whole file at once
        file_string = infile.read()

        # Entry columns are separated by ","
        # Entries are separated by "\n"\

        # Sometimes, there will be "","" used in product description, e.g "Movie Title 2"
        # do not split on such cases
        all_columns = re.split('(?<![0-9a-zA-Z?! ]\")\",\"(?!\"[0-9a-zA-Z])|(?<!\n)\"\n\"(?!\")', file_string)

        # Create dict with row index as key and row as value
        # The dict will be later passed to DataFrame

        all_rows = dict.fromkeys(range(1, 1000000))
        all_rows.update((k, []) for k in range(1, 1000000))
        row = []
        column_counter = 0
        entry_counter = 0

        for column in all_columns:
            # There are 29 columns in entry
            if column_counter == 29:
                # Sometimes there are leftover " in first column
                # get rid of them
                row[0] = row[0].strip('"')

                # DEBUG - if there are any illegal chars in user product description
                # it prints where they are so that we can fix/remove them

                # if is_date(entry[10]) and is_zero_or_one(entry[14]):
                #    print("OK!")

                row = map(replace_f_t, row)
                row = drop_columns(list(row), drop_list)
                if len(row) != 18:
                    print("Row length error, actual len: ", len(row))
                    return

                if entry_counter != 0:
                    all_rows[entry_counter] = row

                row = []
                column_counter = 0
                entry_counter += 1

            row.append(column)
            column_counter += 1

        df = pd.DataFrame.from_dict(all_rows, orient='index')
        df.columns = col
        # Sort the values by ad index
        df['id'] = df['id'].apply(pd.to_numeric)
        df = df.sort_values(['id'])
        name = filename.split('/')[-1] + '.csv'
        df.to_csv(parsed_data_path + name, sep=',', index=False)
    return


def write_all_ads_to_csv(adlist):
    for ad in adlist:
        if not os.path.isfile(raw_data_path + ad):
            continue
        parse_ads_to_csv(ad)
    return


def get_filenames(path):
    """
    Returs the list of all the filenames in directory specified by path
    :param path: the path to directory
    :return: filename list
    """
    return [f for f in listdir(path) if isfile(join(path, f))]


def extract_date(path_str):
    """
    Extracts the date from end of the path_str and converts it to sqlite datetime format.

    :param path_str: The path that ends with date in YYYY_MM_DD format
    :type path_str: str
    :returns: The date in YYYY-MM-DD sqlite datetime format
    """
    path_str = path_str.replace('_', '-')
    path_str = path_str.split('.')[0]
    return "-".join(path_str.split('-')[-3:])


def parse_day_queries(path, conn):
    """
    Parsers all the .csv search queries for given day and inserts them into database
    specified by conn.

    :param path: The path with day's search_queries
    :type path: str
    :param conn: The connection to the database
    :type conn: sqlite3.Connection
    """

    cursor = conn.cursor()
    with open(path) as infile:
        date = extract_date(path)
        reader = csv.reader(infile)
        for category in reader:
            if len(category) != 3:
                continue
            record = [category[0], category[1], category[2], date]
            # print(record)
            q.search_queries_insert(cursor, tuple(record))
    conn.commit()
    return


def parse_queries(db_name):
    """
    Parses all the search queries for given month from 14th to the end of the month
    ands inserts them into the database specified by db_name. The changes are commited
    after inserting all the search queries from the month.

    :param db_name: The name of the database
    """
    conn = _sqlite3.connect(db_path + db_name)

    # Get the folder where the all files from given month are
    path = search_queries_data_path.replace('#', db_name).split('.')[0] + "_01"
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            # TODO use absolute path
            parse_day_queries(str(directory).split('\'')[1] + "/" + str(filename), conn)
    conn.commit()
    return


def fill_db(db_name):
    """
    Inserts all the data for given month into the database specified by the db_name.

    :param db_name: The name of the database

    """
    parse_categories(db_name)
    parse_queries(db_name)
    parse_ads(db_name)
    return


def fill_all_dbs():
    return
