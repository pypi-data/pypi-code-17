# -*- coding: utf-8 -*-
"""
Created on Fri May  5 13:19:33 2017

@author: liujiacheng1
"""

from setuptools import setup, find_packages


setup(

    name='alphaseeker',
    version='0.0.2',

    packages=find_packages(
        exclude=['tests', 'tests.*', '*.tests', '*.tests.*']),
    scripts=['ljc-alpha.py','indexs.py'],

    description='Alpha like ratios calculate ,based on the chinese stock market for now',
    author='Jiacheng Liu',
    author_email='Kevin_ljc@foxmail.com',
    
)
    
    
    
    