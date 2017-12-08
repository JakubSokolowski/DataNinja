import _sqlite3
import csv
import re
import os
import db.queries.insertions as q
from db import db_path
from db import categories_path
from db import ads_data_path
from db import search_queries_data_path


def parse_categories(path):
    """
    Reads all the categories from categories.csv file and inserts them
    into categories table in database specified by path.

    :param path: The path to the database
    :type path: str

    """

    conn = _sqlite3.connect(path)
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
            print(record)
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
