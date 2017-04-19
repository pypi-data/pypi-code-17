"""Code to evaluate a nested list(if any) so that 
each lsit in the main list gets operated and printed. The code uses a recursive function
and the list is passed as a parameter and also a level value to print the nested list with indentation"""
from __future__ import print_function
def print_lol(the_list, level):
    """This for loop iteates to each item in the main list and checks whether that item is a single
    element to print or a list to iterate again through it and if it is a list it begins a level to provide indentation for that list"""    
    for each_item in the_list:
        if isinstance(each_item, list):
            level = level + 1;
            print_lol(each_item, level)
        else:
            for tabs in range(level):
                print ("\t", end=" ")
            print(each_item)
    
