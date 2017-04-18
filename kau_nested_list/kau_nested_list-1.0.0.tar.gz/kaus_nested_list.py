"""Code to evaluate a nested list(if any) so that 
each lsit in the main list gets operated and printed. The code uses a recursive function
and the lsit is passed as a parameter"""

def print_lol(the_list):
    """This for loop iteates to each item in the main list and checks whether that item is a single
    element to print or a list to iterate again through it"""    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
    
