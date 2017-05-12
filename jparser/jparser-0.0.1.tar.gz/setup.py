# coding=utf-8
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='jparser',
    author="Sun, Junyi",
    version='0.0.1',
    license='MIT',

    packages=["jparser"],

    description="A parser which can extract title, content, images from html pages",
                long_description='''
Usage Example:

import urllib2
from jparser import PageModel
html = urllib2.urlopen("http://news.ifeng.com/a/20170512/51084814_0.shtml").read().decode('utf8')
pm = PageModel(html)
print pm.extract()

                ''',

    install_requires=[
        "lxml >= 3.7.1",
    ]
)