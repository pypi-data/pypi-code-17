"""
https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='allinux',
    
    version='0.2.0',
    
    description='Linux command collections',
    long_description='Linux command collections',
    
    url='https://github.com/andrewliqw/python-linux-command',
    
    author='Andrew Li',
    author_email='andrewliqw@outlook.com',
    
    license='MIT',
    
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='python linux command',

    install_requires=[''],

    packages=find_packages('src'),
    package_dir={'':'src'},
)
