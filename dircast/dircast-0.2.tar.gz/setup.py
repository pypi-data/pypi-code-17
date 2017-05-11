import os
import re
from setuptools import setup

# here
here = os.path.abspath(os.path.dirname(__file__))

# rst_path
rst_path = os.path.join(here, 'README.rst')

# rst_data
with open(rst_path, mode='r', encoding='utf-8') as f:
    rst_data = f.read()

# dc_path
dc_path = os.path.join(here, 'dircast.py')

# dc_data
with open(dc_path, mode='r', encoding='utf-8') as f:
    dc_data = f.read()

# ver
m = re.search('^__version__ = \'(.*?)\'$', dc_data, flags=re.MULTILINE)
ver = m.group(1)

# setup
setup(
    
    name = 'dircast',
    
    version = ver,
    
    description = 'Tool for duplicate directories search.',
    
    long_description = rst_data,
    
    author = 'Dmitry Unruh',
    
    author_email = 'dmitryunruh@googlemail.com',
    
    license = 'MIT',
    
    classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4'
    ],
    
    keywords = 'search find duplicate directories folders',
    
    py_modules=['dircast']
    
    )
