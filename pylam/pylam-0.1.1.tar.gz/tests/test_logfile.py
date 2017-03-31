#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pylam


exampleFile0='example_data_files/log.lammps'
exampleFile1='example_data_files/log.lammps.new'
exampleFile2='example_data_files/log.lammps.old'


LF0 = pylam.LogFile(exampleFile0)
LF2 = pylam.LogFile(exampleFile2)
print '='*80

LF0.info()

print '='*80

bl00 = LF0[0]
bl20 = LF2[0]

bl20.info()
print '='*80

#bl00.get_stats()
bl00.print_benchmark()

print '-'*80

#bl20.get_stats()
bl20.print_benchmark()