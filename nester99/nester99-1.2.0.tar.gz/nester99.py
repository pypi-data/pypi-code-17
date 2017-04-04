""" This is the nestor.py module for function print_lol which prints lists that may or may not include nested lists"""

def print_lol(the_list, level=0):
    """This function takes a positional argument called "the_list, which is any python list (of, possibly nested lists). Each data item in the provided list is recursively printed to the screen on its own line"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for num in range(level):
                print("\t", end='')
            print(each_item)
            

