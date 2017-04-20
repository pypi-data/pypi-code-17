from .base import Statement
from pdb import set_trace


class Return(Statement):
    """ Terminate a function """

    def __init__(self, val='', _type='return', *args, **kwargs):
        """
        Args:
            _type (string): type of terminator. Should be one of: 'return', , 'yield', 'pass', '' (or None)
            val (Statement): The Statement that is to be returned
        """
        super(Return, self).__init__(*args, **kwargs)
        self._type = _type if _type is not None else ''
        self.val = Statement.to_statement(val)
        self.line_ending = ''

    def generate(self):
        self.val.generate()
        val = [v for v in self.val.render() if v]
        rendered_return = [self._type]
        rendered_return.extend(val)
        self.code = ' '.join(rendered_return)


class Docstring(Statement):
    """ A triple quoted string """
    def __init__(self, doc_string, *args, **kwargs):
        """
        Args:
            doc_string (string): The string to triple quote
        """
        super(Docstring, self).__init__(*args, **kwargs)
        self.doc_string = doc_string

    def build_renderer(self, *args, **kwargs):
        kwargs['increment'] = 0
        return self.render(*args, **kwargs)

    def generate(self):
        self.code = '"""{}"""'.format(self.doc_string)


class Assignment(Statement):
    """ Assign a value to a name """

    def __init__(self, target=None, value=None, *args, **kwargs):
        """
        Args:
            target (string): The name that will have data assigned to it
            value (string/Statement): The value to be assigned to the target
        """
        super(Assignment, self).__init__(*args, **kwargs)
        self.target = target
        self.value = value

    def generate(self):
        for obj in [self.target, self.value]:
            try:
                obj.generate()
            except AttributeError:
                pass
        self.code = str(self.target) + ' = ' + str(self.value)