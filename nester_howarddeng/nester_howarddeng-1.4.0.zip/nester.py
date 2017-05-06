"""the standard way to include mutiple line comment in your code"""
def print_lol(mm,ident=False,level=-1) :
    if isinstance(mm,list) :
        for each_item in mm :
            print_lol(each_item,ident,level+1)
    else :
        if (ident==True) :
            for num in range(level) :
                print("\t",end='')
        print(mm)
