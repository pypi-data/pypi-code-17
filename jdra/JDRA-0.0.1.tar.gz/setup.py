# -*- coding: utf-8 -*-
"""
Created on Fri May  5 13:19:33 2017

@author: liujiacheng1
"""

from setuptools import setup, find_packages


setup(

    name='JDRA',
    version='0.0.1',

    packages=find_packages(),
    scripts=['clean_data.py','cluster.py','news_len','process.py'],
    description='JD robot-adivisor,Combining the machine learning method with the behaviour finance theory to cluster customers based on the attention list of stocks in chinese market',
    author='Jiacheng Liu',
    author_email='Kevin_ljc@foxmail.com',
    
)
    
    
    
    