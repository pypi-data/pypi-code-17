# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()


setup(
    name='sortedm2m-horizontal-widget',
    version='0.5.0',
    author='Sander van Leeuwen',
    author_email = 'replytosander@gmail.com',
    packages=['sortedm2m_horizontal_widget'],
    include_package_data=True,
    url='https://github.com/svleeuwen/sortedm2m-filter-horizontal-widget',
    license = 'BSD',
    description='Horizontal filter widget for django-sortedm2m',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
    install_requires = ['django-sortedm2m'],
)