"""This is the "nester.py" module, and it provides one function called print_list_elements()
which prints lists that may or may not include nested lists."""

new_list = [1,2,3,[4,[5,6,7]]]
def print_list_elements(the_list):
	"""This function takes a positional argument called "the_list", which is any Python list
	(of, possibly, nested lists). Each data item in the provided list is (recursively) printed
	to the screen on its own line."""
	for item in the_list:
		if isinstance(item,list):
			print_list_elements(item)
		else:
			print(item)
print_list_elements(new_list)