#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
"""
打包的用的setup必须引入，
"""

VERSION = '0.3'

setup(name='textLine_count',
      version=VERSION,
      description="a small program that could count code line numbers",
      long_description='just enjoy',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python line count',
      author='tiantian',
      author_email='tianzhuo_sd@163.com',
      url='https://github.com/amazing-tiantian',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'requests',
      ],
      entry_points={
        'console_scripts':[
            'textLine_count = TLCount.textline_count:main'
        ]
      },
)