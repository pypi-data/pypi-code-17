"""This is the standard way to 
include a muliple-line comment in
your code."""
def print_lol(the_list, level=0, indent=False):
        """This function defined a recursive way
	to print a nested list var加个中文"""
        for each_item in the_list:
                if isinstance(each_item, list):
                    print_lol(each_item, level+1, indent)
                else:
                    if indent:
                            for i in range(level):
                                    print('****',end='')
                    print(each_item)
