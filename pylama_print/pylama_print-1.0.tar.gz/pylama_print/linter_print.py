import ast
import _ast
from pylama.lint import Linter as BaseLinter


DEFAULT_ERR = 'Found `print` call.'


class Linter(BaseLinter):
    """Linter for flagging print() functions."""

    @staticmethod
    def run(path, code=None, params=None, **meta):
        """Check code for print functions or statements.

        :return list: List of errors.
        """
        messages = []

        tree = ast.parse(code, path)

        for node in ast.walk(tree):
            if isinstance(node, _ast.Call):
                try:
                    if node.func.id == 'print':
                        msg = {'lnum': node.lineno, 'text': DEFAULT_ERR}
                        messages.append(msg)
                except AttributeError:
                    pass

        return messages
