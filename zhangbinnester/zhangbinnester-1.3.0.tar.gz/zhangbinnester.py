#encoding:utf-8
def print_lol(the_list,indent = False,Level):
    for each_item in the_list:
        if isinstance(each_item,list):            
            print_lol(each_item,indent,Level+1)
            
        else:
            if indent:
			
				for tab_stop in range(Level):
					print("\t"*Level,end='')         

            print(each_item)




















