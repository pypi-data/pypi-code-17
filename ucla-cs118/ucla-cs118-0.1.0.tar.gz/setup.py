#!/usr/bin/env python
'''Setuptools params'''

import setuptools

setuptools.setup(
    name='ucla-cs118',
    version='0.1.0',
    description='Network controller for the class project of UCLA CS118 class',
    url='http://web.cs.ucla.edu/classes/spring17/cs118/',
    author='Alex Afanasyev',
    author_email='aa@cs.ucla.edu',
    license='GPL3+',
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Internet",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
)
