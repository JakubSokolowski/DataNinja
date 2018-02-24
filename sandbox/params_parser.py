# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:49:49 2017

@author: Adrian
"""

import _sqlite3
import re

import matplotlib.pyplot as plt
import numpy as np

conn = _sqlite3.connect('2016_11.db')
cursor = conn.cursor()

def params_parser(params):
    par_list=re.split("<=>|<br>", params)
    parsed_params=dict()
    par_list[
        [i for i in range(0, len(par_list)) if par_list[i] == "price" and par_list[i + 1] == 'price'][0]] = "price_type"
    for i in range(0, int((len(par_list) / 2))):
        parsed_params[par_list[2*i]]=par_list[2*i+1]
    return parsed_params


# params="price<=>price<br>price<=>20<br>state<=>new<br>type<=>woman<br>size<=>l"

def ad_params(params):
    par_list = re.split("<=>|<br>", params)
    params = set()
    for i in range(0, int((len(par_list) / 2))):
        params.add(par_list[2 * i])
    return params


# command='SELECT params FROM ads LIMIT 100000'

def all_params(command):
    params_counter = dict()
    for ad in cursor.execute(command):
        for param in ad_params(str(ad[0])):
            if param in params_counter:
                params_counter[param] = params_counter[param] + 1
            else:
                params_counter[param] = 1
    return (params_counter)


data = all_params(command)
indexes = np.arange(len(data.keys()))
plt.bar(indexes, data.values(), 0.2)
plt.xticks(indexes, data.keys(), rotation=90)
plt.show()
￼
