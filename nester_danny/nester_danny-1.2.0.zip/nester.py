def print_list(list1,indent=False,level=0):
    for char in list1:
        if isinstance(char,list):
            print_list(char,indent,level+1)
        else:
            if indent:
                for i in range(level):
                    print ("\t",end="")    
            print (char)

        
