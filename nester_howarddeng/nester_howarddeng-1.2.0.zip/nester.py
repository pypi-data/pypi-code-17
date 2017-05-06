"""the standard way to include mutiple line comment in your code"""
def print_lol(mm,level) :
    if isinstance(mm,list) :
        for each_item in mm :
            print_lol(each_item,level+1)
    else :
        for num in range(level) :
            print("\t",end='')
        print(mm)
