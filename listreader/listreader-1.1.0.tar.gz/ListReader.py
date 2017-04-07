'''This is a 'nester.py' module which has a function 'print_lol'
that is used to print the message'''

def read(theList, level):
        '''This function takes in a list and prints the items in the list.
A second optional argument called "level" is used to insert a tab stop when a nested list
is encountered.'''
        for listItem in theList:
                if(isinstance(listItem, list)):
                        read(listItem, level+1)
                else:
                        for tabStop in range(level):
                                print('\t', end='')
                        print(listItem)
