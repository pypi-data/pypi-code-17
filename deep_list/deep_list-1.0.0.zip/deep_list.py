''' his is a sample module 'deep_list.py' that provide a function called print_lol() which print lists that may or may not include nested lists. '''
def print_dem(n):
    ''' This function takes one positional argument called 'n', which is any python list (possibly nested). Each data item in the list provied is (recursively) displayed on the screen on its own line. '''
    for i in n:
        if isinstance(i, list):
            print_dem(i)
        else:
            print(i)



            
