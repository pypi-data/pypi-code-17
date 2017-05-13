"""This is the standard way to 
include a muliple-line comment in
your code."""
def print_lol(the_list, indent=False, level=0):
        """This function defined a recursive way
	to print a nested list var加个中文"""
        for each_item in the_list:
                if isinstance(each_item, list):
                    print_lol(each_item, indent, level+1)
                else:
                    if indent:
                            for i in range(level):
                                    print('****',end='')
                    print(each_item)
