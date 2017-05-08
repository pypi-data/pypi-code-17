"""Example module.

Docstring style reference: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Example usage as executable:
	$ <virtual-env-name>/bin/python src/modulelevel.py
"""

class ExampleClass(object):
	def __init__(self):
		pass


def moduleLevelFunction(arg):
	"""Example module level function.

	Args:
		arg (str): Example argument implementation.
	"""
	return arg

if __name__ == '__main__':
	moduleLevelFunction("Hello world!")
