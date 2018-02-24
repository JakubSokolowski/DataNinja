# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 14:05:28 2017

@author: Adrian
"""
import _sqlite3

conn = _sqlite3.connect('2016_11.db')
cursor = conn.cursor()

def is_searched(search, ad_title):
    return (True)

def title_search_counter(ad):
    for search in cursor.execute('SELECT * FROM queries'):
        if (search[1] == ad[0] or search[1] == ''):
            if (is_searched(search[0], ad[1]) == 1):
                title_searches = title_searches + search[2]
    return (title_searches)
        

for ad in cursor.execute('SELECT category_id, title FROM ads'):
    print(title_search_counter(ad))


def category_search_counter(ad):
    for search in cursor.execute('SELECT * FROM queries'):
        if (search[0] == ''):
            if (search[1] == ad[0]):
                category_searches = category_searches + search[2]
    return (category_searches)

for ad in cursor.execute('SELECT category_id, title FROM ads'):
    print(category_search_counter(ad))
