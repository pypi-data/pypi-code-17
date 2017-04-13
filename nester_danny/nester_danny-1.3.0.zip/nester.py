def print_list(list1,indent=False,level=0,fn=sys.stdout):
    for char in list1:
        if isinstance(char,list):
            print_list(char,indent,level+1,fn)
        else:
            if indent:
                for i in range(level):
                    print ("\t",end="",file=fn)    
            print (char,file=fn)

        
