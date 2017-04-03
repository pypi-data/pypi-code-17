''' his is a sample module 'deep_list.py' that provide a function called print_dem() which print lists that may or may not include nested lists. '''
def print_dem(n, level):
    ''' This function takes one positional argument called 'n', which is any python list (possibly nested). Each data item in the list provied is (recursively) displayed on the screen on its own line. A second argument called "level" is used to insert tab-stops when a nested list is encounted.'''
    for i in n:
        if isinstance(i, list):
            print_dem(i, level)
        else:
            for tab_stop in range(level + 1):
                print("\t", end='')
            print(i)



