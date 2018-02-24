import _sqlite3


# creating ads database

# 25 Categories:
# FORMAT AND DESCRIPTION
# DATE FORMAT: YYYY-MM-DD HH:MM:SS
# DATE is NUMERIC in SQLITE

# 1  "id",                     - INTEGER
# 2  "region_id",              - INTEGER
# 3  "category_id",            - INTEGER
# 4  "subregion_id",           - INTEGER
# 5  "district_id",            - INTEGER
# 6  "city_id",                - INTEGER
# 7  "accurate_location",      - BOOLEAN: if 1, user added from mobile app, and selected location from map
# 8  "user_id",                - INTEGER:
# 9  "sorting_date",           - DATE:
# 10 "created_at_first",       - DATE:
# 11 "valid_to",               - DATE: when will be deactivated
# 12 "title",                  - TEXT
# 13 "description",            - TEXT: short description 256 char
# 14 "full_description",       - TEXT:
# 15 "has_phone",              - BOOLEAN
# 16 "params",                 - TEXT?: various params of add, example, price, state, type, brand
# 17 "private_business",       - BOOLEAN:
# 18 "has_person",             - BOOLEAN:
# 19 "photo_sizes",            - TEXT ? JSON: json array with photo sizes
# 20 "paidads_id_index",       - INTEGER: type of paid promotion of the ad
# 21 "paidads_valid_to",       - DATE: expiration date of the promotion
# 22 "predict_sold",           - DATE? :
# 23 "predict_replies",        - INTEGER:
# 24 "predict_views",          - INTEGER:
# 25 "reply_call",             - INTEGER: DO NOT TRAIN - number of calls (14 days)
# 26 "reply_sms",              - INTEGER: DO NOT TRAIN - number of SMS messages (14 days)
# 27 "reply_chat",             - INTEGER: DO NOT TRAIN - number of chat messages (14 days)
# 28 "reply_call_intent",      - INTEGER: DO NOT TRAIN - number of attempts to call the seller (14 days)
# 29 "reply_chat_intent"       - INTEGER: DO NOT TRAIN - number of attempts to send a chat message (open chat window) (14 days)


# integer, text  database_name = 'ads_2016_11_01'


def create_ads_db(db_name):
    conn = _sqlite3.connect(db_name)
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
    conn.commit()
    conn.close()
    return
