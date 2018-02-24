def create_model_table(conn):
    """
        Creates table that holds all the unique combinations of phrase, category id that were
        searched in given month and the session_count for that combination
        :param conn: The connection to sqlite database
        :type conn: sqlite3.Connection.
        :return:

        """
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE model(
                                phase text,
                                region_id integer,
                                subregion_id,
                                category_id text,
                                session_count int)""")
