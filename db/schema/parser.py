import _sqlite3
import csv
import re
import os
from db import db_path
from db import categories_path
from db import ads_data_path
from db import search_queries_data_path
import db.queries.insertions as q


# Parses the categories.csv file and adds it to the database
def parse_categories(db_name):
    conn = _sqlite3.connect(db_name)
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
            q.categories_insert(cursor,tuple(record))
    conn.commit()
    return


def replace_f_t(x):
    if x == "f":
        return "0"
    elif x == "t":
       return "1"
    else:
        return x

# Parses ads for given month
def parse_ads(db_name):
    conn = _sqlite3.connect(db_path.replace('#',db_name))
    cursor = conn.cursor()

    path = ads_data_path.replace('#',db_name)
    with open(path) as infile:
        # Read whole file at once
        # WARNING : might crash with really big ones, idk
        file_string = infile.read()

        # Entry columns are separeted by ","
        # Entries are separeted by "\n"\

        # Sometimes, there will be "","" used in product description, e.g "Movie Title 2"
        # do not split on such cases
        all_columns = re.split('(?<![0-9a-zA-Z?! ]\")\",\"(?!\"[0-9a-zA-Z])|(?<!\n)\"\n\"(?!\")',file_string)

        entry = []
        column_counter = 0
        entry_counter = 0

        for column in all_columns:
            # There are 29 columns in entry
            if column_counter == 29:
                # Sometimes there are leftower " in first column
                # get rid of them
                entry[0] = entry[0].strip('"')

                # DEBUG - if there are any illegal chars in user product description
                # it prints where they are so that we can fix/remove them
                print(entry)

                #if is_date(entry[10]) and is_zero_or_one(entry[14]):
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

def extract_date(filepath):
    filepath = filepath.replace('_','-')
    filepath = filepath.split('.')[0]
    return "-".join(filepath.split('-')[-3:])


def parse_day_queries(path, conn):
    cursor = conn.cursor()
    with open(path) as infile:
        date = extract_date(path)
        reader = csv.reader(infile)
        for category in reader:
            if len(category) != 3:
                continue;
            record = [category[0], category[1], category[2], date]
            print(record)
            q.search_queries_insert(cursor, tuple(record))
    conn.commit()
    return


def parse_queries(db_name):
    conn = _sqlite3.connect(db_path + db_name)

    # Get the folder where the all files from given month are
    path = search_queries_data_path.replace('#', db_name).split('.')[0] + "_01"
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            # uglyy hack
            parse_day_queries(str(directory).split('\'')[1] +"/"+ str(filename), conn)
    conn.commit()
    return


def fill_db(db_name):
    parse_categories(db_name)
    parse_queries(db_name)
    parse_ads(db_name)
    return


def fill_all_dbs():
    return


#("lmao")
#parse_ads("2017_02")

#fill_db("2017_01.db")
db_name = "2016_11.db"
#parse_categories(db_path + db_name)
parse_queries(db_name)
