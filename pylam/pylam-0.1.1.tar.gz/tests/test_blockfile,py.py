#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pylam.base

class MyBlockFile(pylam.base.BlockFile):

    def __init__(self, filename):
        self.tmp = None
        super(MyBlockFile, self).__init__(filename)

    def _parseLine(self, line, no):
        if "[data]" in line:
            self.tmp = no + 1
        if "[end data]" in line:
            self.addBlock(fline=self.tmp, lline=no-1, header_line=str('Block {0:d}'.format(len(self))))


blockfile = MyBlockFile('example_data_files/bfile.txt')

#print len(blockfile)

# for block in blockfile:
#     print block.header_line
#     print block.startLineIndex
#     print block.endLineIndex

print blockfile[0].data
