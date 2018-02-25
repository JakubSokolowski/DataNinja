import _sqlite3
import time
from collections import defaultdict
from collections import namedtuple

import pandas as pd

import db.data.sampler as smp
from db import db_path
from db import model_path


def match_query_to_desc(conn):
    # Dict query_phrase,category_id : list of ads that match query
    # Dict ad_id : list of query_phrases

    # Create query_ad map - maps combination to ad id's
    queries = smp.sample_queries(conn, 'MAX')

    Combination = namedtuple("Combination", ["phrase", "category_id"])

    q_list = list(zip(queries['phrase'], queries['category_id']))
    # Dict mapping combinations of phrase -> category_id to session_count
    qsc_list = list(zip(queries['phrase'], queries['category_id']))
    combinations = []
    for el in qsc_list:
        # Convert tuple to named tuple
        combinations.append(Combination(*el))
    # print(qsc_list)
    q_session_count = dict(zip(combinations, queries['session_count']))
    print(q_session_count)

    combinations = []
    for el in q_list:
        # Convert tuple to named tuple
        combinations.append(Combination(*el))

    # Update all the keys in list with empty list value
    query_ad = defaultdict(list)
    query_ad.update((k, []) for k in combinations)

    ads = pd.read_sql_query("Select id,category_id,title from ads limit 10000", conn)

    # Create dict with ad_id and all the phrases that match the ad
    query_list = ads['id'].tolist()
    ad_query = defaultdict(list)
    ad_query.update((k, []) for k in query_list)

    # Create dict with ad_id and total hit count from search queries
    ad_hit_count = dict()
    ad_hit_count.update((k, 0) for k in query_list)

    # Iterate over each ad tuple
    # 1 - id, 2 - category_id, 3 - title
    for search in ads.itertuples():
        # Split the ad title into words
        for word in search[3].split():
            # Check if the combination of word,category_id is in dict
            comb = Combination(word, str(search[2]))
            if comb in query_ad:
                query_ad[comb].append(search[1])
                ad_query[search[1]].append(word)
                ad_hit_count[search[1]] += q_session_count[comb]

    match_count = 0
    ad_count = 0
    for key, value in query_ad.items():
        if value:
            match_count += 1
            ad_count += len(value)

    print("Number of combinations phrase/category_id that found matches: ")
    print(match_count)
    print("Total number of ads that matches some search query")
    print(ad_count)

    match_count = 0
    ad_count = 0
    for key, value in ad_query.items():
        if value:
            match_count += 1

    print("Matched ads:")
    print(match_count)
    # print(ad_hit_count)

    empty = 0
    full = 0
    for key, value in ad_hit_count.items():
        if value:
            full += 1
            print(key, value)
        else:
            empty += 1

    print("Part matching: ", full / (empty + full))

    return


def match_phrase_to_desc(conn):
    # Dict query_phrase,category_id : list of ads that match query
    # Dict ad_id : list of query_phrases

    # Create query_ad map - maps ad_ids to phrases
    queries = smp.sample_queries(conn, 'MAX')
    query_ad = defaultdict(list)
    query_ad.update((k, []) for k in queries['phrase'])

    ads = pd.read_sql_query("Select id,category_id,title from ads", conn)

    # Create dict with ad_id and all the phrases that match the ad
    query_list = ads['id'].tolist()
    ad_query = defaultdict(list)
    ad_query.update((k, []) for k in query_list)

    # Create dict with ad_id and total hit count from search queries
    ad_hit_count = dict()
    ad_hit_count.update((k, 0) for k in query_list)

    q_session_count = dict(zip(queries['phrase'], queries['session_count']))

    # Iterate over each ad tuple
    # 1 - id, 2 - category_id, 3 - title
    for search in ads.itertuples():
        # Split the ad title into words
        for word in search[3].split():
            # Check if the combination of word,category_id is in dict
            if word in query_ad:
                query_ad[word].append(search[1])
                ad_query[search[1]].append(word)
                ad_hit_count[search[1]] += q_session_count[word]

    df = pd.DataFrame({'keys': list(ad_hit_count.keys()), 'values': list(ad_hit_count.values())})
    df.to_csv(model_path + "ad_hits.csv", index=False, sep=";")


def match_browsing(conn):
    # Count the just browsing sessions

    empty_searches = dict();
    cat_list = pd.read_sql_query("select category_id from categories", conn)['category_id'].tolist()
    empty_searches.update((k, 0) for k in cat_list)

    queries = pd.read_sql_query("select phrase,category_id, session_count from queries", conn)

    for row in queries.itertuples():
        if row[1] == '' and row[2] != '':
            empty_searches[int(row[2])] += row[3]
    # df = pd.DataFrame({'keys': list(empty_searches.keys()), 'values': list(empty_searches.values())})

    ads = pd.read_sql_query("Select id, category_id from ads", conn)

    sessions = []
    for row in ads.itertuples():
        sessions.append(empty_searches[row[2]])

    ads['empty_sessions'] = pd.Series(sessions).values
    header = ["id", "empty_sessions"]

    ads.to_csv(model_path + "empty_sessions.csv", columns=header, index=False, sep=";")
    return


def sort_hits(name):
    df = pd.read_csv(model_path + name, sep=';')
    print(df)
    df = df.sort_values(['keys'])
    # df.sort(['keys'])
    print(df)
    df.to_csv(model_path + "sorted_ad_hits.csv", index=False, sep=";")

conn = _sqlite3.connect(db_path + '2016_11.db')
start = time.time()
sort_hits("ad_hits.csv")
end = time.time()

print(end - start)
