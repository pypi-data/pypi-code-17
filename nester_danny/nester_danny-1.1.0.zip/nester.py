def print_list(list1,level):
    for char in list1:
        if isinstance(char,list):
            print_list(char,level+1)
        else:
            for i in range(level):
                print ("\t",end="")    
            print (char)
a=[1,2,[3,4,5,[6,7,8,9]]]
print_list(a,0)
        
