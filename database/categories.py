import _sqlite3
import csv

db_name = "/home/jakub/DataNinja/data/database/ads_2016_11_01.db"
conn = _sqlite3.connect(db_name)
cursor = conn.cursor()


def create_categories_db():
    conn = _sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE categories (
                    category_id integer primary key,
                    name text not null,
                    parent_id int default null)""")
    conn.commit()
    conn.close()
    return


def add_new_category(entry):
    cursor.execute("""INSERT INTO categories VALUES(?,?,?)""", entry)
    return


# create_categories_db()
category_path = "/home/jakub/DataNinja/data/categories.csv"


# Asummed file format: id, parent_id, name
def parse_categories(filename):
    with open(filename) as infile:
        reader = csv.reader(infile)
        firstline = True
        for category in reader:
            if firstline:
                firstline = False
                continue
            print(category)
            list = [category[0], category[2], category[1]]
            add_new_category(tuple(list))
    conn.commit()
    return

# parse_categories(category_path)
