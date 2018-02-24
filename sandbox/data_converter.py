# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 21:18:07 2018

@author: Adrian
"""

import _sqlite3
import json
from datetime import time

import numpy as np
import pandas as pd
from sandbox.params import params_parser

from db.data.sampler import sample_ads

conn = _sqlite3.connect('2016_11.db')
data = sample_ads(conn, 1000)

def db_to_csv(query):
    conn = _sqlite3.connect('2016_11.db')
    data = pd.read_sql_query(query, conn)
    data.to_csv('ads.csv', sep=';')
 
def photos_parser(photo_sizes):
    photo_sizes = photo_sizes.replace('""', '"')
    data = json.loads(photo_sizes)
    num_of_photos = len(data)
    return (num_of_photos)

def num_of_photos(data):
    all_photos = data['photo_sizes'].apply(str)
    num_of_photos = []
    for i in range(len(all_photos)):
        try:
            num_of_photos.append(photos_parser(all_photos[i]))
        except:
            num_of_photos.append(0)
    return (pd.DataFrame({'num_of_photos': num_of_photos}))


def time_since_creation(data):
    time_since_creation = pd.DataFrame({"time_since_creation": (
            pd.to_datetime(data['sorting_date']) - pd.to_datetime(data['created_at_first'])).astype('timedelta64[h]')})
    time_since_creation[time_since_creation < 0] = 0
    return (time_since_creation)

def time_on_frontpage(data_sorted):
    time_on_frontpage = data['sorting_date'][39:len(data_sorted)]
    return (pd.DataFrame({'time_on_frontpage': time_on_frontpage}))

def traffic_level(data):
    l = np.zeros(len(data))
    twos = np.array((pd.to_datetime(data['sorting_date']).dt.time >= time(18, 00)) & (
            time(22, 00) >= pd.to_datetime(data['sorting_date']).dt.time))
    l[twos] = 2
    ones = np.array((pd.to_datetime(data['sorting_date']).dt.time >= time(8, 00)) & (
            time(18, 00) >= pd.to_datetime(data['sorting_date']).dt.time))
    l[ones] = 1
    return (pd.DataFrame({'traffic_level': l}))

def params_parser(params):
    par_list = re.split("<=>|<br>", params)
    parsed_params = dict()
    if 'price' in par_list:
        par_list[par_list.index('price')] = "price_type"
    for i in range(0, int((len(par_list) / 2))):
        parsed_params[par_list[2 * i]] = par_list[2 * i + 1]
    return parsed_params

def params(data):
    price_type, price, state, Type = ([] for i in range(4))
    for i in range(len(data)):
        params = data['params'][i]
        par = params_parser(params)
        try:
            price_type.append(par['price_type'])
        except KeyError:
            price_type.append(0)
        try:
            price.append(par['price'])
        except KeyError:
            price.append(0)
        try:
            state.append(par['state'])
        except KeyError:
            state.append(0)
        try:
            Type.append(par['type'])
        except KeyError:
            Type.append(0)
    params = pd.DataFrame({'price_type': price_type,
                           'price': price,
                           'state': state,
                           'type': Type})
    return (params)
   
def promo_level(data):
    promo_lvl = np.zeros(len(data))
    promo_lvl[data['paidads_id_index'] == 3] = 1
    promo_lvl[data['paidads_id_index'] == 4] = 2
    promo_lvl[data['paidads_id_index'] == 85] = 3
    return (pd.DataFrame({'promotion_level': promo_lvl}))
    
####################################################################
def convert_data(query):
    conn = _sqlite3.connect('2016_11.db')
    df = pd.read_sql_query(query, conn)
    params_df = params(df)
    df = pd.concat([df, params_df, time_since_creation(df), traffic_level(df), num_of_photos(df), promo_level(df)],
                   axis=1)
    df = df.drop(['params', 'district_id', 'sorting_date', 'created_at_first', 'valid_to', 'photo_sizes', 'reply_call',
                  'reply_sms', 'reply_chat', 'reply_call_intent', 'reply_chat_intent', 'description',
                  'full_description', 'paidads_valid_to', 'accurate_location', 'has_person', 'paidads_id_index'], 1)
    df.to_sql('ads_new', conn)


convert_data("select * from ads limit 1000")
