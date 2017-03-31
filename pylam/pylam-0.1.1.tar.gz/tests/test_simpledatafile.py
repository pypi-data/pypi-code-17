#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pylam

exampleFile='example_data_files/standart.dat'
#exampleFile='example_data_files/ave_time_scalar.dat'

SDF = pylam.SimpleDataFile(exampleFile)

print len(SDF)

print 'header:', SDF.header
print 'header line:', SDF.header_line

print '*'*80

data = SDF.getRow(10)

print data
print type(data)
print SDF.properHeader

print '*'*80

print SDF.getColumnByName('Step')