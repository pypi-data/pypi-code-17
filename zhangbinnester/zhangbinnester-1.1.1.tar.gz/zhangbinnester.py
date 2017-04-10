#encoding:utf-8

def print_lol(the_list,Level):
    for each_item in the_list:
        if isinstance(each_item,list):           
            print_lol(each_item,Level+1)           
        else:           
            for tab_stop in range(Level):
                print("\t","end=")         

            print(each_item)





















