"""Questions about the built-in types.

https://docs.python.org/3.6/library/stdtypes.html
"""

import textwrap

from ..base import Question, WrongAnswer


class FindAllSubclasses(Question):
    """Find all subclasses of a class.

    https://docs.python.org/3.6/library/stdtypes.html?#class.__subclasses__
    """

    def get_question_text(self):
        """Get the question text."""
        return textwrap.dedent(
            """\
            Find all subclasses of a class.

            Assume you have a class called `BaseClass`, and you also have some other classes that inherit from `BaseClass`.

            Find all classes that inherit from `BaseClass` and store them as a list in a variable called `subclasses`.
            """
        )

    def check_answer(self, answer):
        """Check if an answer is correct"""
        class BaseClass(object):
            pass

        class ChildClass1(BaseClass):
            pass

        class ChildClass2(BaseClass):
            pass

        answer_locals = {'BaseClass': BaseClass}
        try:
            exec(answer, {}, answer_locals)
            if answer_locals['subclasses'] == BaseClass.__subclasses__():
                return True
            else:
                raise WrongAnswer('Answer is incorrect.')
        except Exception as e:
            raise WrongAnswer(e)

    def get_correct_answers(self):
        """Get an example answer that is correct."""
        return ["subclasses = BaseClass.__subclasses__()"]

    def get_wrong_answers(self):
        return ['']
