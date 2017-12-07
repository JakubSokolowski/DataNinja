# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 19:49:39 2017

@author: Adrian
"""

text = """{"1":{"w":934,"h":700},"2":{"w":934,"h":700},"3":{"w":934,"h":700}}"""

import json
from pprint import pprint

data = json.loads(text)
pprint(data)

for i in data:
    print(data[i])

text="""{""1"":{""w"":934,""h"":700},""2"":{""w"":934,""h"":700},""3"":{""w"":934,""h"":700}}"""
text.replace('""','"')


def is_good(photo):
    return True 

def photos_parser(photo_sizes):
    data=json.loads(photo_sizes)
    num_of_photos=len(data)
    num_of_good_photos=0
    for i in data:
       photo=(data[i]['w'],data[i]['h']) 
       if is_good(photo):
           num_of_good_photos=j+1
    return(num_of_photos,num_of_good_photos)       