#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sptempdir import TemporaryDirectory


#
print("========================================================")
print("Example 1:")
print("---------")

with TemporaryDirectory(prefix="prefbegin_", suffix="_suffend") as temp:
	print('temp.name:', temp.name)  # retrieve the name temporary directory
	print('Inside:', os.path.exists(temp.name))

print('Outside:', os.path.exists(temp.name))

#
print("========================================================")
print("Example 2:")
print("---------")

temp = TemporaryDirectory()
print('temp.name:', temp.name)  # retrieve the name temporary directory
print('Tempdir exists:', os.path.exists(temp.name))

temp.rmtemp()  # manually remove temporary directory
print('Tempdir exists:', os.path.exists(temp.name))

#
print("========================================================")
print("Example 3:")
print("---------")

temp = TemporaryDirectory(delete=False)
print('temp.name:', temp.name)  # retrieve the name temporary directory
print('Tempdir exists:', os.path.exists(temp.name))

temp.rmtemp()  # manually remove temporary directory
print('Tempdir exists:', os.path.exists(temp.name))

#
print("========================================================")
print("Example 4:")
print("---------")

temp = TemporaryDirectory(dir="/home/user/Desktop")
print(temp.name)  # retrieve the name temporary directory
