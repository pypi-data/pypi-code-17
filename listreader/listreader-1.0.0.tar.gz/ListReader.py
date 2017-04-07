'''This is a 'nester.py' module which has a function 'print_lol'
that is used to print the message'''

def read(theList):
        '''This function takes in a list and prints the items in the list'''
        for listItem in theList:
                if(isinstance(listItem, list)):
                        read(listItem)
                else:
                        print(listItem)
