
def print_lol(the_list,indent=False,level=0):
	"""
	这个函数取一个位置参数，名为“the_list”。
	 这可以是任何python列表（也可以是包含嵌套列表的列表）
	所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项各站一行。
	"""
	for e_item in the_list:
		if isinstance(e_item,list):
			print_lol(e_item,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
				    print('--------------------')
			print(e_item)
