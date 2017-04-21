#!env/bin/python
from sourcerer import Statement
from sys import stderr
from yapf.yapflib.yapf_api import FormatCode
from pdb import set_trace


class Document(Statement):
    """ All content is rooted in this base document

    All a document really is, is a statement with a \\n line ending and an output method.
    """

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.line_ending = '\n'

    def output(self, output_file_name='', yapf=True, **yapfkwargs):
        """ Write out the syntax tree """

        syntax_string = self.line_ending.join(self)
        if yapf:
            syntax_string = FormatCode(syntax_string, **yapfkwargs)[0]
        if not output_file_name:
            return syntax_string
        else:
            try:
                with open(output_file_name, 'w') as output:
                    output.write(syntax_string)
            except (IOError, OSError) as e:
                stderr.write(str(e))
                raise
