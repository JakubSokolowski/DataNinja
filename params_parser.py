# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:49:49 2017

@author: Adrian
"""
import re
def params_parser(params):
    par_list=re.split("<=>|<br>",params)    
    parsed_params=dict()
    par_list[[i for i in range(0,len(par_list)) if par_list[i]=="price"][0]]="price_type"
    for i in range(0,int(len(par_list)/2)):
        parsed_params[par_list[2*i]]=par_list[2*i+1]
    return parsed_params

params="price<=>price<br>price<=>20<br>state<=>new<br>type<=>woman<br>size<=>l"
params_parser(params)
