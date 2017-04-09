"""Questions about the built-it functions.

Docs: https://docs.python.org/3.6/library/functions.html
"""

import textwrap

from ..base import Question


class AbsoulteValue(Question):
    """Get the absolute value of a number.

    https://docs.python.org/3.6/library/functions.html#abs
    """

    def get_question_text(self):
        return textwrap.dedent(
            """\
            Get the absolute value of a number.

            Assume you have a variable called `some_number`, which contains a number.

            Write some code that evaluates to the absolute value of that number.
            """
        )

    def check_answer(self, answer):
        test_numbers = [0, 1, -1, 0.0, 0.1, -0.1]
        try:
            return all(
                abs(some_number) == eval(answer, {}, {'some_number': some_number})
                for some_number in test_numbers
            )
        except:
            return False

    def get_an_answer(self):
        return 'abs(some_number)'


class TrueForAll(Question):
    """Check if all items are true.

    https://docs.python.org/3.6/library/functions.html#all
    """

    def get_question_text(self):
        return textwrap.dedent(
            """\
            Check if all items are true.

            Assume you have a collection called `items`.

            Write some code that evaluates to True if every item in the collection if true.
            """
        )


    def check_answer(self, answer):
        test_cases = [
            [True, True, True],
            [True, True, False],
        ]
        try:
            return all(
                all(case) == eval(answer, {}, {'items': case})
                for case in test_cases
            )
        except:
            return False

    def get_an_answer(self):
        return 'all(items)'

