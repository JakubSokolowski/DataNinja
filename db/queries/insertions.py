
def categories_insert(cursor, record):
    cursor.execute("""INSERT INTO categories VALUES(?,?,?)""", record)
    return


def ads_insert(cursor, record):
    cursor.execute("""INSERT INTO ads VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", record)
    return


def search_queries_insert(cursor, record):
    cursor.execute("""INSERT INTO queries VALUES(?,?,?,?)""", record)
    return;
