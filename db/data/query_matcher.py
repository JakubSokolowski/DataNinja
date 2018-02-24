import _sqlite3
import time
from collections import defaultdict
from collections import namedtuple

import pandas as pd

import db.data.sampler as smp
from db import db_path


def match_query_to_desc(conn):
    # Dict query_phrase,category_id : list of ads that match query
    # Dict ad_id : list of query_phrases

    # Create query_ad map - maps combination to ad id's
    start = time.time()
    queries = smp.sample_queries(conn, 'MAX')
    end = time.time()
    print("Time to fetch queries: ", end - start)

    Combination = namedtuple("Combination", ["phrase", "category_id"])

    q_list = list(zip(queries['phrase'], queries['category_id']))
    combinations = []
    for el in q_list:
        # Convert tuple to named tuple
        combinations.append(Combination(*el))

    query_ad = defaultdict(list)
    query_ad.update((k, []) for k in combinations)

    # Create ad_query_map

    start = time.time()
    ads = pd.read_sql_query("Select id,category_id,title from ads limit 50000", conn)
    end = time.time()
    print("Time to fetch ads: ", end - start)

    query_list = ads['id'].tolist()
    ad_query = defaultdict(list)
    ad_query.update((k, []) for k in query_list)

    start = time.time()
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

    end = time.time()
    print("Time to match queries to ads: ", end - start)

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
    return


def title_matches(title, phrase):
    return phrase in title


conn = _sqlite3.connect(db_path + '2016_11.db')
start = time.time()
match_query_to_desc(conn)
end = time.time()

print(end - start)
