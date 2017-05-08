# -*- coding: utf-8 -*-
"""
Created on Sun May 07 15:56:32 2017

@author: AJ
"""

from setuptools import setup, find_packages

setup(
    name = 'DummyPackageAJ',
    version = '1.2.0',
    description = 'A sample Python project',
    author = 'Weineaj',
    author_email = 'weiner.arthur.j@gmail.com',
    license = 'MIT',
    
    classifiers = [
        # How mature is this project?  Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        
        # Indicate who your project is intended for
        'Intended Audience :: Other Audience',
        'Topic :: Artistic Software',
        
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        
        # Specify the Python versions you support here.  In particular, ensure
        # that you indicate whether you support Python 2, 3, or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    
    keywords = 'sample doNothing',
    packages = find_packages(exclude=['contrib', 'docs', 'tests*']),
)    
