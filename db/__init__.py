from pathlib import Path

# Relative path to all the .db and .csv files in project
# Assumed to by two folders up from the db module folder
# ..../main_data_path/DataNinja/db
# /main_data_path/ ----> data  ------> ads
#                  |           ------> database
#                  |           ------> search_queries
#                  |
#                  ----> DataNinja --> db
#                                  --> docs
#                                  --> notebooks
#                                  --> sandbox

main_data_path = str(Path(__file__).parents[2]) + "/data/"

db_path = main_data_path + 'database/'
ads_data_path = main_data_path + 'ads/#/001_anonimized'
search_queries_data_path = main_data_path + 'search_queries/#'
categories_path = main_data_path + 'categories.csv'

# print(db_path)
# print(ads_data_path)
# print(search_queries_data_path)
# print(categories_path)


