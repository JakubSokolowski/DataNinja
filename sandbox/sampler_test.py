import _sqlite3
import time

import pandas as pd

from db import db_path

conn = _sqlite3.connect(db_path + '2016_11.db')

start = time.time()
df = pd.read_sql_query("Select city_id from ads", conn)
df = df['city_id'].value_counts()
print(df)
end = time.time()

print(end - start)
