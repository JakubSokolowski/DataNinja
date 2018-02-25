import pandas as pd

import db.queries.string_quries as sq


def sample_ads(conn, size, random=False):
    """
    Returns sample of ads table specified by connection
    :param conn: Connection to sql database
    :type conn: sqlite3.Connection
    :param size: sample size, set to 'MAX' to return whole table
    :param random: specifies whether the sample will be random
    :return: the pandas.DataFrame with sample
    """
    query = sq.all_ads_limit.replace('#', str(size))
    if size == 'MAX':
        query = sq.all_ads
    if random:
        query = sq.all_ads_random.replace('#', str(size))
    return pd.read_sql_query(query, conn)


def sample_queries(conn, size, random=False):
    """
        Returns sample of queries table specified by connection
        :param conn: Connection to sql database
        :type conn: sqlite3.Connection
        :param size: sample size, set to 'MAX' to return whole table
        :param random: specifies whether the sample will be random
        :return: the pandas.DataFrame with sample
    """
    query = sq.all_queries_limit.replace('#', str(size))
    if size == 'MAX':
        query = sq.all_queries
    if random:
        query = sq.all_ads_random.replace('#', str(size))
    return pd.read_sql_query(query, conn)
