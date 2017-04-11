
"""
This is "nester.py" module, 
which provides a funtion named print_lol. 
the function is designed for print list, 
may include(or not) nest list.
"""


def print_lol(the_list,indent=False,level=0,fn=sys.stdout):
    """
    This function pick a location parameter, named "the_list". 
    it can be any python list (can be nest list which include another nest list).
    by use this function, each per data item in the list will be output to the screen in a nested.
    each data item takes up one line.
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fn)
        else:
            if indent:
                for tab_stop in range(level):
                    print ("\t",end='', file=fn)
            print(each_item,file=fn)



# movies = ['\"A\"', 'B', 'C', [1, 2, 3]]
# movies.insert(1, 1981)
# movies.insert(3, 1971)
# movies.insert(5, 1985)
# movies.insert(5, [1, 9, ["x", "y", "z"], 8, 5])
# print (movies)
# print ("===================================")
# print_lol(movies,1)