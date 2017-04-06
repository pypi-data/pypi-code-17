def print_lol(the_list,level):
    """这个函数取一位参数，名为‘the_list’，这个可以是任何python列表。所指定的列表中的每个数据项会输出到屏幕上"""
    
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
                
        else:
            for tab_stop in range(level):
                print("\t',end=")
            print(each_item)
            
                    
                    
