# encoding: utf8

"""
Created on 2016.01.13

@author: ZoeAllen
"""
import time
from script.mod.test import Test

print('import mod.hi.py')

def go_hi():
    print('go')


def run_hi(**kwargs):
    t = Test()
    t.start()
    import sys
    for r in sys.path:
        print(r)
    while 1:
        print('say hi')
        time.sleep(5)
