import _sqlite3

from db import db_path


def create_categories_table(conn):
    """
    Creates table that holds all the product categories in sqlite database specified by conn.

    :param conn: The connection to sqlite database.
    :type conn: sqlite3.Connection.

    """
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE categories (
                       category_id integer primary key,
                       name text not null,
                       parent_id int default null)""")
    conn.commit()


def create_ads_table(conn):
    """
    Creates table that holds ads from one month in sqlite database specified by conn.

    :param conn: The connection to sqlite database.
    :type conn: sqlite3.Connection.

    """
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE ads (
                               id integer primary key,
                               region_id integer,
                               category_id integer,
                               subregion_id integer,
                               district_id integer,
                               city_id integer,
                               accurate_location boolean,
                               user_id,
                               sorting_date datetime,
                               created_at_first datetime,
                               valid_to datetime,
                               title text,
                               description text,
                               full_description text,
                               has_phone boolean,
                               params text,
                               private_business boolean,
                               has_person boolean,
                               photo_sizes text,
                               paidads_id_index integer,
                               paidads_valid_to integer,
                               predict_sold datetime,
                               predict_replies integer,
                               predict_views integer,
                               reply_call integer,
                               reply_sms integer,
                               reply_chat integer,
                               reply_call_intent integer,
                               reply_chat_intent integer) 
                               """)


def create_search_queries_table(conn):
    """
    Creates table that holds all the search queries from one month
    in sqlite database specified by connection.

    :param conn: The connection to sqlite database.
    :type conn: sqlite3.Connection.

    """

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE queries (
                           phrase text,
                           category_id text,
                           session_count int,
                           query_date datetime)""")
    return


def create_db(conn):
    """
    Creates ads, categories and queries tables in database specified by connection and
    closes that connection.

    :param conn: The connection to sqlite database.
    :type conn: sqlite3.Connection.

    """
    create_categories_table(conn)
    create_ads_table(conn)
    create_search_queries_table(conn)
    conn.close()


def create_all_dbs():
    """
    Creates all databases for months from 2016_11 to 2017_10.

    """

    db_name = '2016_1#.db'
    for i in range(1, 3):
        path = db_path + str.replace(db_name, '#', str(i))
        create_db(_sqlite3.connect(path))

    db_name = '2017_0#.db'
    for i in range(1, 10):
        path = db_path + str.replace(db_name, '#', str(i))
        create_db(_sqlite3.connect(path))

    db_name = '2017_10.db'
    create_db(_sqlite3.connect(db_path + db_name))
