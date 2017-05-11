from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='bitsprikol',
    version=__import__('bits').__version__,
    url='http://4plitka.esy.es/',
    author='kusegorplay',
    packages=find_packages(),
    long_description='Крутая программа! Very cool program!',
    entry_points={
        'console_scripts':
            ['bits = bits.core:main']
    }
)
