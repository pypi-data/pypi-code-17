#!/usr/bin/env python

import os
try:
    the_file = open('sketch.txt')
    for each_line in the_file:
        (who, what) = each_line.split(":", 1)
        print (who, end='')
        print (" said", end='')
        print (what, end='')
except:
    pass
the_file.close()

