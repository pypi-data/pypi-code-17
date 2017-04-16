#!/usr/bin/env python

try:
    the_file = open('sketch.txt')
    for each_line in the_file:
        try:
            (who, what) = each_line.split(":", 1)
            print (who, end='')
            print (" said", end='')
            print (what, end='')
        except ValueError:
            pass
    the_file.close()
except IOError:
    print('The data file is missing')
