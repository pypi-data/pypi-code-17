def print_lol(the_list,indent=False,level=0,fn=sys.stdout):
    """这个函数取一位参数，名为‘the_list’，这个可以是任何python列表。所指定的列表中的每个数据项会输出到屏幕上"""
    
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fn)
                
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end="",file=fn)      
            print(each_item,file=fn)
            
                    
                    
