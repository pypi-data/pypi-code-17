"""Questions about the built-in exceptions.

Docs: https://docs.python.org/3.6/library/exceptions.html
"""

from ..base import Question, WrongAnswer


class CauseExceptionMixin(object):
    """A mixin for questions about causing exceptions.

    Implements functionality that is common among exception-causing questions.
    """

    def __init__(self):
        self.exception = Exception

    def get_question_text(self):
        return (
            'Cause an {exception_name}.\n\n'
            'Write some code that will raise an {exception_name}.\n\n'
            'Your code may not contain the words `raise` or `exec`.'
        ).format(exception_name=self.exception.__name__)

    def check_answer(self, answer):
        for illegal_word in ['raise', 'exec']:
            # `exec` is banned because it can be used to construct `raise`.
            if illegal_word in answer:
                raise WrongAnswer('Illegal word used.')
        try:
            exec(answer, {}, {})
        except self.exception:
            return True
        except Exception as e:
            raise WrongAnswer('Wrong exception was raised: %s' % e)
        raise WrongAnswer('No exceptions were raised.')

    def get_wrong_answers(self):
        return ['raise {}'.format(self.exception.__name__)]


class CauseAssertionError(CauseExceptionMixin, Question):
    """Cause an AssertionError.

    https://docs.python.org/3.6/library/exceptions.html#AssertionError
    """

    def __init__(self):
        self.exception = AssertionError

    def get_correct_answers(self):
        return ['assert(False)']


class CauseAttributeError(CauseExceptionMixin, Question):
    """Cause an AttributeError.

    https://docs.python.org/3.6/library/exceptions.html#AttributeError
    """

    def __init__(self):
        self.exception = AttributeError

    def get_correct_answers(self):
        return ['"".foo']


class CauseEOFError(CauseExceptionMixin, Question):
    """Cause an EOFError.

    https://docs.python.org/3.6/library/exceptions.html#EOFError
    """

    def __init__(self):
        self.exception = EOFError

    def get_correct_answers(self):
        return [(
            'import StringIO\n'
            'import sys\n'
            'sys.stdin = StringIO.StringIO("")\n'
            'input()\n'
        )]
