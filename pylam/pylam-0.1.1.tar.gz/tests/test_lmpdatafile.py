#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pylam





#LDFO = pylam.LammpsDataFile(filename='example_data_files/bmimbr.data', atom_style='full')

#LDFO = pylam.LammpsDataFile(filename='example_data_files/lj.data', atom_style='atomic')

LDFO = pylam.LammpsDataFile(filename='example_data_files/bmimbr.data', atom_style='molecular')

print '\n' +'='*80 +'\n\n'

#print LDFO

LDFO.xyz_print()

L = (float(LDFO.Vol))**(1/3)
print LDFO.Vol