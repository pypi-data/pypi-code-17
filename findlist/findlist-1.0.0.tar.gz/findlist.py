#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 22:15:49 2017

@author: brucejiang
"""

def print_lol(list_name):
    for each_item in list_name:
        if type(each_item)==list:
            print_lol(each_item)
        else:print(each_item)
