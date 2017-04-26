''' show a list with indent which you can input or just leave it '''
def print_lol(the_list, indent=False, tab=0):
	for item in the_list:
		if(isinstance(item,list)):
			print_lol(item, indent, tab+1)
		else:
                        if(indent == True):
                                for t in range(tab):
                                        print("\t", end='')
                        print(item)

