import _sqlite3
import re

# Database connection and cursor, hardcoded
conn = _sqlite3.connect('ads_2016_11_01.db')
cursor = conn.cursor()

# Replaces the characters t and f with 1 and 0
def replace_f_t(x):
    if x == "f":
        return "0"
    elif x == "t":
       return "1"
    else:
        return x

# Adds new entry to the database
# Kinda unsafe
def add_new_entry(entry):
    cursor.execute("""INSERT INTO ads VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", entry)
    return

# Parses given number of entries from text file and adds them to db
def parse(filename, entry_num):
    with open(filename) as infile:
        # Read whole file at once
        # WARNING : might crash with really big ones, idk
        file_string = infile.read()

        # Entry columns are separeted by ","
        # Entries are separeted by "\n"\
        # Assumption here, is that user does not have this sets of characters
        # in his product description.
        all_columns = re.split('","|"\n"', file_string)

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
                    entries = map(replace_f_t, entry)
                    # Add the entry to the db
                    # WARNING - unfiltered tuple input, assuming that
                    # none of the OLX users is named DROP TABLE ADS
                    if entry_counter != 0:
                        add_new_entry(tuple(entries))

                    entry = []
                    column_counter = 0

                    entry_counter += 1

                    if entry_counter == entry_num:
                        conn.commit()
                        return

            entry.append(column)
            column_counter += 1
        conn.commit()
    return