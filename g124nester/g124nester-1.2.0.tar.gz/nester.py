#!/usr/bin/env python
''' This is the nester.py module, and it proviedes one function called print_lol() which prints the lists that may 
        or may not include nested lists'''

movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, 
                ["Graham Chapman", ["Michael Palin", "John Cleese",
                        "Terry Gilliam", "Eric Idle", "Terry Jones"]]]


def print_lol(the_list, indent=False, level=0):
    ''' This function takes positional argument called the "the_list", which is any python list( of possibly nested lists). 
        Each data item in the provided lists is recursively printed to the screen on its own line'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)

print_lol(movies, True, 0)
