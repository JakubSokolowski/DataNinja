import _sqlite3

#creating ads database

#25 Categories:
# FORMAT AND DESCRIPTION
# DATE FORMAT: YYYY-MM-DD HH:MM:SS
# DATE is NUMERIC in SQLITE

# "id",                     - INTEGER
# "region_id",              - INTEGER
# "category_id",            - INTEGER
# "subregion_id",           - INTEGER
# "district_id",            - INTEGER
# "city_id",                - INTEGER
# "accurate_location",      - BOOLEAN: if 1, user added from mobile app, and selected location from map
# "user_id",                - INTEGER:
# "sorting_date",           - DATE:
# "created_at_first",       - DATE:
# "valid_to",               - DATE: when will be deactivated
# "title",                  - TEXT
# "description",            - TEXT: short description 256 char
# "full_description",       - TEXT:
# "has_phone",              - BOOLEAN
# "params",                 - TEXT?: various params of add, example, price, state, type, brand
# "private_business",       - BOOLEAN:
# "has_person",             - BOOLEAN:
# "photo_sizes",            - TEXT ? JSON: json array with photo sizes
# "paidads_id_index",       - INTEGER: type of paid promotion of the ad
# "paidads_valid_to",       - DATE: expiration date of the promotion
# "predict_sold",           - DATE? :
# "predict_replies",        - INTEGER:
# "predict_views",          - INTEGER:
# "reply_call",             - INTEGER: DO NOT TRAIN - number of calls (14 days)
# "reply_sms",              - INTEGER: DO NOT TRAIN - number of SMS messages (14 days)
# "reply_chat",             - INTEGER: DO NOT TRAIN - number of chat messages (14 days)
# "reply_call_intent",      - INTEGER: DO NOT TRAIN - number of attempts to call the seller (14 days)
# "reply_chat_intent"       - INTEGER: DO NOT TRAIN - number of attempts to send a chat message (open chat window) (14 days)



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
