#!env/bin/python

from sys import argv
from yaml import loads
from functools import wraps
"""
I don't know if I even need this file anymore
Also I'm pretty sure I haven't tested or even run this code yet.
"""

# Number of spaces in a tab. It's 4.
TAB_WIDTH = 4


class Generator(object):
    """ Write declarations out to a file.

    A declaration should be one indentation scope.
    eg.
        scope 1:
            def hello_world():
        scope 2:
            return thing
    """

    def __init__(self, output_filename="out.txt", tab_width=TAB_WIDTH):
        """
        Args:
            output_filename (str): Name of the file to write to.
            tab_width (int): Number of spaces per tab. It's 4.
        """
        self.output_filename = output_filename
        self.tab_width = tab_width
        # How many tabs to indent by
        self.tab_depth = 0
        # Should we shutdown and close the output file?
        self.finished = False

    def inject_indent(self):
        """ Calculate the spaces required for the current indentation level

        Return (str): n number of spaces
        """
        return (" " * 4) * self.tab_depth

    def process(self, declaration):
        """ Iterate over scopes in a declaration and build them """
        code = ""
        for scope in declaration:
            self.tab_depth += 1
            code = "\n".join([code, self.inject_indent(), scope.declare()])
        self.tab_depth = 0
        return code

    def build(self, declaration=None):
        with open(self.output_filename, 'w') as output_file:
            while not self.finished:
                if declaration is not None:
                    declaration = yield self.process(declaration)

    def kill(self):
        """ Return StopIteration from build generator and reset parameters """
        self.finished = True
        self.tab_depth = 0
        next(self.build)

    def new_file(self, filename=None):
        """ Reset generator with new output file

        Args:
            filename (str): Name of new file to write to. If None, overwrite default file
        """
        self.kill()
        self.finished = False
        self.output_filename = filename if filename else self.output_filename


if __name__ == "__main__":
    gen = Generator()
    code = gen.build()

    # some fake data
    code_objs = []

    for obj in code_objs:
        code.send(obj)

    gen.kill()
