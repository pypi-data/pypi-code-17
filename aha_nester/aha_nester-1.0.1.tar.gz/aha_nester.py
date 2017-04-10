"""This is the standard waty to
include a multiple-line comment in
your code."""

def print_lol(the_list):
	for a in the_list:
		if isinstance(a, list):
			print_lol(a)
		else:
			print(a)

