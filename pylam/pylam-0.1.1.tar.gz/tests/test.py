#!/usr/bin/env python
# -*- coding: utf-8 -*-



exampleFile='example_data_files/log.lammps'


def pBox():
    pass

def pAtoms():
    pass

test_dict = {'orthogonal box': pBox, 'atoms': pAtoms}

print test_dict.keys()
for key in test_dict.keys():
    print key

myf = open(exampleFile,'r')
for line in myf:
    for key in test_dict.keys():
        if key in line:
            print '*', key, line
