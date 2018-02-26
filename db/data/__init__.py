from pathlib import Path

raw_data_path = str(Path(__file__).parents[3]) + "/months-data-raw/"
parsed_data_path = str(Path(__file__).parents[3]) + "/months-data-parsed/"
parsed_queries_path = str(Path(__file__).parents[3]) + "/queries-data-parsed/"
# 1  id integer primary key,
# 2  region_id integer,
# 3  category_id integer,
# 4  subregion_id integer,
# 5  district_id integer,
# 6  city_id integer,
# 7  accurate_location boolean,
# 8  user_id,
# 9  sorting_date datetime,
# 10 created_at_first datetime,
# 11 valid_to datetime,
# 12 title text,
# 13 description text,
# 14 full_description text,
# 15 has_phone boolean,
# 16 params text,
# 17 private_business boolean,
# 18 has_person boolean,
# 19 photo_sizes text,
# 20 paidads_id_index integer,
# 21 paidads_valid_to integer,
# 22 predict_sold datetime,
# 23 predict_replies integer,
# 24 predict_views integer,
# 25 reply_call integer,
# 26 reply_sms integer,
# 27 reply_chat integer,
# 28 reply_call_intent integer,
# 29 reply_chat_intent integer

# List of not needed columns
drop_list = [5, 7, 11, 13, 14, 18, 25, 26, 27, 28, 29]

# Names of all the columns needed for processing
col = ['id', 'region_id', 'category_id', 'subregion_id', 'city_id',
       'user_id', 'sorting_date', 'created_at_first',
       'title', 'has_phone', 'params', 'pricate_business',
       'photo_sizes', 'paidads_id_index', 'paidads_valid_to',
       'predict_sold', 'predict_replies', 'predict_views']
