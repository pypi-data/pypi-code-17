''' This is the nester.py module, and it proviedes one function called print_lol() which prints the lists that may 
        or may not include nested lists'''

def print_lol(the_list):
    ''' This function takes positional argument called the "the_list", which is any python list( of possibly nested lists). 
        Each data item in the provided lists is recursively printed to the screen on its own line'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

