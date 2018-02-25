import _sqlite3

import pandas as pd

from db import db_path
from db import model_path

conn = _sqlite3.connect(db_path + '2016_11.db')
cursor = conn.cursor()

query = """SELECT 
                        id, 
                        region_id, 
                        category_id, 
                        subregion_id, 
                        city_id, 
                        user_id,
                        sorting_date,
                        created_at_first,
                        has_phone,
                        params,
                        private_business,
                        photo_sizes,
                        paidads_id_index,
                        paidads_valid_to,
                        predict_replies,
                        predict_sold,
                        predict_views
                        from ads"""

df = pd.read_sql_query(query, conn)
df.to_csv(model_path + "model_raw.csv", index=False, sep=";")
