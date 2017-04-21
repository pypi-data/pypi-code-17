#!env/bin/python
import re
from numbers import Number


class Statement(object):
    """ A line of code

    A Statement is a line of code that may or may not have a child Scope
    """

    def __init__(self, code='', scope=None, whitespace='', line_ending=''):
        """
        self.code is the actual line of code that this object represents.
        self.scope (if any) is the child scope of this statement. eg.
         self.code ->   while 1:
                      |     do thing 1
         self.scope ->|     do thing 2
                      |     do thing 3

        Args:
            code (str): The code that will be represented
        """
        self.code = code
        self.scope = scope if scope is not None else []
        self.whitespace = whitespace if whitespace else ' ' * 4
        self.line_ending = line_ending

    def __iter__(self):
        renderer = self.build_renderer()
        for node in renderer:
            yield node

    def __str__(self):
        return self.line_ending.join(self)
        return self.code

    def __repr__(self):
        return self.line_ending.join(self)
        return self.code

    def add_child(self, child):
        """ Append a child to this statements scope

        Args:
            child (Statement): The child to append
        """
        if isinstance(child, Statement):
            self.scope.append(child)
        else:
            raise Exception("child " + child + " is not a Statement")

    def add_children(self, child_list):
        """ A convenience function to load multiple children into this scope

        Args:
            child_list (list): a list of children to append to this objects scope
        """
        for child in child_list:
            if isinstance(child, list):
                self.add_children(child)
            else:
                self.add_child(child)

    def create_lineage(self, lineage):
        """ Create a hierarchical lineage of children with this object as the oldest member. eg.
        children = [c1, [c2.1, c2.2], c3]
        result -- self (top level)
                    |-> c1
                        |-> c2.1
                            c2.2
                            |-> c3
        """
        current_node = self
        for child in lineage:
            if child:
                if isinstance(child, list):
                    current_node.add_children(child)
                    current_node = child[-1]
                else:
                    current_node.add_child(child)
                    current_node = child

    def from_parent(self, parent):
        """ Append this statement to the scope of a parent statement

        Args:
            parent (Statement): The parent to append this statement to
        """
        if isinstance(parent, Statement):
            parent.scope.append(self)
        else:
            raise Exception("parent " + parent + " is not a Statement")

    def from_lineage(self, lineage):
        """ Create a hierarchical list of parents with this object as the youngest decentant

        Lineage will be arranged in the order the parents are provided. eg.
        parents = [p1, p2, p3]
        result -- p1 (top level)
                  |->p2
                     |->p3
                        |->self
        In this example the top level parent would be at scope level n+1 and
        this object would be at scope level n+4.

        Args:
            lineage (list): a hierarchical list of parents for this object.
        """
        current_node = self
        lineage.reverse()
        for parent in lineage:
            current_node.from_parent(parent)
            current_node = parent

    def format(self):
        """ Abstract function to format properties this object """
        pass

    def generate(self, *args, **kwargs):
        """ Abstract function to set self.code """
        pass

    def build_renderer(self, *args, **kwargs):
        """ Overwrite this function to customize how render should be called
        for particular objects
        """
        return self.render(*args, **kwargs)

    def render(self, level=-1, increment=1):
        """ Return this statement and all children recursively

        Args:
            level (int): The indentation level to set for this statement
            increment (int): The number of indentation levels for the child scope
        """
        self.format()
        self.generate(level=level, increment=increment)
        yield "{}{}{}".format(self.whitespace * level, self.code,
                              self.line_ending)
        for child in self.scope:
            #child.format()
            #child.generate()
            child_renderer = child.build_renderer(level=level + increment)
            while 1:
                try:
                    yield next(child_renderer)
                except StopIteration:
                    break

    @staticmethod
    def to_statement(item):
        """ Convert a string to a Statement

        If the argument passed is already a Statement or Statment derivitive, return it unaltered
        If the argument passed is a Non-Statment, return input as a Statement

        Args:
            item (str, Statement): The object to be converted to a Statement
        """
        if isinstance(item, Statement):
            return item
        else:
            return Statement(item)

    @staticmethod
    def make_valid(name):
        """ Convert a string to a valid python name

        Args:
            name (string): The name to be converted
        """
        name = re.sub('[^0-9a-zA-Z_]', '', str(name))  # Remove invalid characters
        name = re.sub('^[^a-zA-Z_]+', '', str(name))   # Remove leading characters until we find a letter or underscore
        return name


class Name(Statement):
    """ A variable/function/class/... name

    n = Name("helloworld") -> (unquoted) helloworld

    NOTE:
        Unless the validate flag is set to False, this will reformat a name if
        it is not a proper python variable name
        n = Name("123*helloworld") -> (unquoted) helloworld

    Args:
        validate (bool): Should name be converted to valid python variable name?
    """
    def __init__(self, code, validate=True, *args, **kwargs):
        super(Name, self).__init__(*args, **kwargs)
        self.line_ending = ''
        self.code = self.make_valid(code) if validate else code


class Str(Statement):
    """ A quoted string

    Args:
        single (bool): Should use single quotes?

    s = Str("hello world") -> literal 'hello world'
    """

    def __init__(self, code, single=False, *args, **kwargs):
        super(Str, self).__init__(*args, **kwargs)
        self.line_ending = ''
        self.code = self.string_args(code, single)

    def string_args(self, args, single):
        """ Apply single or double quotes to the strings provided.

        Args:
            args (string): A string to be quoted
            single (bool): Use single quotes rather than double
        """

        self.base = '"{}"'
        self.quote_type = '"'
        if single:
            self.base = "'{}'"
            self.quote_type = "'"
        escaped = "\\{}".format(self.quote_type)
        if isinstance(args, Str):
            args = str(args).strip(args.quote_type)
        if isinstance(args, str) or isinstance(args, Statement):
            args = str(args).replace(self.quote_type, escaped)
            return self.base.format(args)


class Num(Statement):
    """ A number. Signed Int, Float, Long, whatever.

    n = Num("4") -> 4

    n = Num(4) -> 4

    n = Num(4.0) -> 4.0
    """

    def __init__(self, code, *args, **kwargs):
        super(Num, self).__init__(*args, **kwargs)
        self.line_ending = ''
        self.code = str(code)