# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 19:49:39 2017

@author: Adrian
"""

import json

text="""{""1"":{""w"":934,""h"":700},""2"":{""w"":934,""h"":700},""3"":{""w"":934,""h"":700}}"""
text = text.replace('""', '"')

def is_good(photo):
    return True 

def photos_parser(photo_sizes):
    photo_sizes = photo_sizes.replace('""', '"')
    data=json.loads(photo_sizes)
    num_of_photos=len(data)
    return (num_of_photos)


photos_parser(text)
