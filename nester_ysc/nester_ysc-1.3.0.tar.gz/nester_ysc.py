def print_items(the_list,indent=False,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_items(each_item,indent,level+1)
		else:
			if indent:
				for tab_c in range(level):
					print('\t',end='')
			print(each_item)
