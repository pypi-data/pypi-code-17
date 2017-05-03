def print_all(a_list):
	for a in a_list:
		if isinstance(a,list):
			for b in a:
				print_all(b)
		else:
			print(a)

