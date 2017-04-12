'''This is a 'nester.py' module which has a function 'print_lol'
that is used to print the message'''

import sys

def read(theList, indent= False, level= 0, fh= sys.stdout):
        '''This function takes in a list and prints the items in the list.
A second optional argument called "level" is used to insert a tab stop when a nested list
is encountered.'''
        for listItem in theList:
                if(isinstance(listItem, list)):
                        read(listItem, indent, level+1, fh)
                else:
                        if(indent):
                                for tabStop in range(level):
                                        print('\t', end='', file= fh)
                        print(listItem, file= fh)
