#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pylam.base

exampleFile='example_data_files/test.txt'
ifile = pylam.base.IndexedFile(exampleFile)

print len(ifile)  # returns the total number of lines

lines = ifile.getLines(5, 9)

print lines

print type(lines)

for line in ifile:
    print line[0:16]

# print 'len :', len(IF)
# print '_fileByteSize:', IF._fileByteSize
# print '1st line:', IF[0]
# print IF._getOffsets(len(IF)-1,len(IF)-1)
#
# print IF._getOffsets(0,0)
# print len(IF[0])
#
# for i in range(0,5):
#     print IF[i]
#
# print '='*80





