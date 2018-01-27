import _sqlite3

import db.data.sampler as sampler
from db import db_path


def create_queries_summary_table(conn):
    """
    Creates table that holds all the unique combinations of phrase, category id that were
    searched in given month and the session_count for that combination
    :param conn: The connection to sqlite database
    :type conn: sqlite3.Connection.
    :return:

    """
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE queries_summary(
                            phase text,
                            category_id text,
                            session_count int)""")


def fill_query_summary_table(conn):
    """
    Combines all the search_query data for given month - sums all the session_count for each
    combination of phrase-category_id and inserts them into table queries_summary
    :param conn: The connection to sql database
    :type conn: sqlite3.Connection
    """
    df = sampler.sample_queries(conn, 'MAX')
    df = df.groupby(['phrase', 'category_id']).sum()
    df = df.sort_values('session_count', ascending=False)
    df.to_sql('queries_summary', conn, if_exists='replace', index=True)


def update_db(conn):
    """
    Adds missing tables to the database specified by connection and closes that connection.
    Missing tables are the tables added during development. Current "missing tables" :
        queries_summary: session counts for all the unique combinations phrase-category_id

    :param conn: The connection to sqlite database
    :type: sqlite3.Connection.

    """
    fill_query_summary_table(conn)
    conn.close()


def update_all_dbs():
    """
    Updates all the databases with missing tables
    """

    db_name = '2016_1#.db'
    for i in range(1, 3):
        path = db_path + str.replace(db_name, '#', str(i))
        update_db(_sqlite3.connect(path))

    db_name = '2017_0#.db'
    for i in range(1, 10):
        path = db_path + str.replace(db_name, '#', str(i))
        update_db(_sqlite3.connect(path))

    db_name = '2017_10.db'
    update_db(_sqlite3.connect(db_path + db_name))

# Example usage
# con = _sqlite3.connect(db_path + "2016_11.db")
# update_db(con)
