# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 22:43:13 2017

@author: Adrian
"""
import _sqlite3

conn = _sqlite3.connect('2016_11.db')
cursor = conn.cursor()


def select_from_category(category, limit=1000):
    command = """WITH RECURSIVE cte (
        category_id,
        name,
        parent_id
    )
    AS (
        SELECT category_id,
               name,
               parent_id
          FROM categories
         WHERE name = '@'
        UNION ALL
        SELECT p.category_id,
               p.name,
               p.parent_id
          FROM categories p
               INNER JOIN
               cte ON p.parent_id = cte.category_id
    )
    SELECT 
          *
      FROM ads
     WHERE category_id IN (
               SELECT category_id
                 FROM cte
        
           ) LIMIT #""".replace('@', category).replace('#', str(limit))
    for row in cursor.execute(command):
        print(row)


select_from_category('Ubrania')
