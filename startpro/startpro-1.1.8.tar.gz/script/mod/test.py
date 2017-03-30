# encoding: utf8

"""
Created on 2016.01.13

@author: ZoeAllen
"""
from startpro.core.process import Process

print('import mod.test.py')


class Test(Process):
    name = 'hi.inner'

    def __init__(self):
        print('init hi.inner')

    def run(self, **kwargvs):
        print('check')
        print('run', kwargvs)

    def start(self):
        print('start')
