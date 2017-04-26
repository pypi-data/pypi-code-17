''' this is a zhushi......'''
def print_lol(the_list, tab:0):
	''' again a zhushi'''
	for item in the_list:
		if(isinstance(item,list)):
			print_lol(item, tab+1)
		else:
                        for t in range(tab):
                                print("\t", end='')
                        print(item)

