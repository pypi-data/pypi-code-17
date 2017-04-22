'''
This module prints all the items in a list,
including the nested lists' factor
'''

def print_nest(the_list, indent=False, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):

            #level+=1
            print_nest(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    #print('\t', end='')
                    print('    ', end='')
            print(each_item)
