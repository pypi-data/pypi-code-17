''' his is a sample module 'deep_list.py' that provide
a function called print_dem() which print lists that
may or may not include nested lists. '''
def print_dem(n, indent=False, level=0, fh=sys.stdout):
    ''' This function takes one positional argument called 'n', which is any
    python list (possibly nested). Each data item in the list provied is
    (recursively) displayed on the screen on its own line. A second argument
    called "level" is used to insert tab-stops when a nested list is encounted.

    The fourth argument 'sys.stdout' is a default value that print to the screen
    of pc if no file object is specified when the function is invoked'''
    for i in n:
        if isinstance(i, list):
            print_dem(i, indent, level + 1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
            print(i, file=fh)



