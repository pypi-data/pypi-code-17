#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pylam

#exampleFile='example_data_files/temp.dat'
#exampleFile='example_data_files/ave_time_scalar.dat'
#exampleFile='example_data_files/standart.dat'
exampleFile='example_data_files/chunk1D.dat'

FBF = pylam.FixBlockFile(exampleFile)

print '='*80

FBF.info()

print '='*80

DB = FBF[0]


print type(DB)

print '='*80

FBF[0].showStat()

print '='*80

FBF[0].info()


print '='*80


newTable = FBF.blocks2cols('v_temp', fix=['Chunk','Coord1'])

newTable.write('b2cTest.dat')
