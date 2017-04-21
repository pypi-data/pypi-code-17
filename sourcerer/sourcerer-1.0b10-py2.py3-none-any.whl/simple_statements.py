from .base import Statement
from .modules import Document
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

    def generate(self, *args, **kwargs):
        self.val.generate(*args, **kwargs)
        val = [v for v in self.val.render() if v]
        rendered_return = [self._type]
        rendered_return.extend(val)
        self.code = ' '.join(rendered_return)


class Docstring(Statement):
    """ A triple quoted string """
    def __init__(self, doc_string="", extended="", extras=None, *args, **kwargs):
        """Docstring builder. Supports google style Doc strings.

        Docstring supports google style markup. The Docstring sections
        can be defined by passing a dict into the extras argument.
        The format is a dict with the section name as the key and a list of
        dicts of parmeters as the vaules.
        The parameter dict has three optional keys:
            id - the parameter name. ex. an function argument name
            param_type - a type for the parameter. ex int
            description - a description of the parameter
        Example:
            {"Args": [{"id":"arg1", "param_type":"string", "description":"the first argument"},
                     {"id":"phone_num", "param_type":"int", "description":"users phone number without punctuation"}],
                     {"id":"address", "description":"users address"}],
             "Returns": [{"param_type":"string", "description":"The customers name"}]}
        Will build out:
            Args:
                arg1 (string): the first argument
                phone_num (int): users phone number without punctuation
                address: users address

            Returns:
                string: The customers name

        Args:
            doc_string (string): The summary line
            extended (string): The extended description
            extras (dict): The input, outputs, raises, etc...
        """
        super(Docstring, self).__init__(*args, **kwargs)
        self.doc_string = doc_string
        self.extended = extended
        self.extras = extras
        self.doc_string_body = Statement('"""{}'.format(doc_string), line_ending="\n")

    def build_renderer(self, *args, **kwargs):
        kwargs['increment'] = 0
        return self.render(*args, **kwargs)

    def generate(self, *args, **kwargs):
        self.create_main_string()
        self.create_sections()
        level = kwargs['level']
        self.doc_string_body.add_child(Statement('"""'))
        output = [s for s in self.doc_string_body.render(level=level-1)]
        self.code = self.doc_string_body.line_ending.join(output)

    def create_main_string(self):
        if self.extended:
            self.doc_string_body.add_child(Statement(self.extended))

    def create_sections(self):
        if self.extras is not None:
            needs_extra_space = bool(self.extended)
            for block, params in self.extras.items():
                section = Statement("{}:".format(block))
                for param in params:
                    section.add_child(self.create_doc_section_param(**param))
                if needs_extra_space:
                    self.doc_string_body.add_children([ Statement(''), section])
                    needs_extra_space = False
                else:
                    self.doc_string_body.add_children([section])

    def create_doc_section_param(self, id='', param_type='', description=''):
        """ Create a parameter line for a section.

        A parameter line for an 'Args:' section could look like: 'arg1 (int): user data'

        Args:
            id (str): Identifier that the line is describing (for example, an argument name)
            param_type (str): The type for the id (for example, int)
            description (str): A string that describes the use of the id

        """

        id_fmt = "{}"
        param_type_fmt = "{}"
        desc_fmt = ": {}"

        if param_type:
            if id:
                param_type_fmt = " ({})".format(param_type_fmt)
            else:
                param_type_fmt = "({})".format(param_type_fmt)

        id = id_fmt.format(id) if id else ''
        param_type = param_type_fmt.format(param_type) if param_type else ''
        description = desc_fmt.format(description) if description else ''
        return Statement("{}{}{}".format(id, param_type, description))


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

    def generate(self, *args, **kwargs):
        for obj in [self.target, self.value]:
            try:
                obj.generate(*args, **kwargs)
            except AttributeError:
                pass
        self.code = str(self.target) + ' = ' + str(self.value)