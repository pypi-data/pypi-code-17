def print_all(the_list):
	for each_i in the_list:
		if isinstance(each_i,list):
			print_all(each_i)
		else:
			print(each_i)