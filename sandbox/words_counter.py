# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 23:57:53 2017

@author: Adrian
"""


import _sqlite3

from nltk.tokenize import word_tokenize

conn = _sqlite3.connect('ads_2016_11_01.db')
cursor = conn.cursor()

command="""WITH RECURSIVE cte (
    category_id,
    name,
    parent_id
)
AS (
    SELECT category_id,
           name,
           parent_id
      FROM categories
     WHERE name = 'Ubrania'
    UNION ALL
    SELECT p.category_id,
           p.name,
           p.parent_id
      FROM categories p
           INNER JOIN
           cte ON p.parent_id = cte.category_id
)
SELECT 
       title
  FROM ads
 WHERE category_id IN (
           SELECT category_id
             FROM cte
    
       ) LIMIT 1000"""


def words_counter(command):
    word_dict=dict()
    for row in cursor.execute(command):
            tokenized_row = word_tokenize(str(row))
            for word in tokenized_row:
                word=str.lower(word)
                if len(word)>1:
                    if word in word_dict:
                        word_dict[word]=word_dict[word]+1
                    else:
                        word_dict[word]=1
    return list(sorted(word_dict.items(), key=lambda x: -x[1]))
      

word_freq = words_counter(command)
word_freq[1:100]
most_freq=[i[0] for i in word_freq[1:40]]
