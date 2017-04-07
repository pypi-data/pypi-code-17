def print_lol(the_hhe):
	for each_item in the_hhe:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
