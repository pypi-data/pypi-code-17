from __future__ import print_function
import os
import sys
from colorama import Fore

if sys.version_info.major == 2:
    _input = raw_input
else:
    _input = input


class Interact:

    def __init__(self, prompt=': ', newline=False, color=None):
        self.prompt = prompt
        self.newline = newline
        self.color = color

    def _get_color(self, attr):
        if not attr:
            return None
        return getattr(Fore, attr.upper())

    def _colored(self, text, color):
        color = self._get_color(color)
        return '{}{}{}'.format(color, text, Fore.RESET)

    def _ask(self, question, default=None, color=None, strip=False, lower=False,
             upper=False, title=False, prompt=None, **kwargs):
        '''
        Asks the user a question.

        :param question: the question to ask
        :param default: a default value, or None
        :param color: the question text color
        :param strip: whether to strip leading and trailing whitespace
        :param lower: lowercase the result
        :param upper: uppercase the result
        :param title: Title Case The Result
        :return: the inputted text
        '''
        color = color or self.color

        if default is not None:
            question = '{} ({})'.format(question, default)

        if color:
            color = self._get_color(color)
            sys.stdout.write(color)

        if self.newline:
            print(question)
        else:
            sys.stdout.write(question)

        if prompt is False:
            pass
        elif prompt is not None:
            sys.stdout.write(prompt)
        elif self.prompt is not None:
            sys.stdout.write(self.prompt)

        if color:
            sys.stdout.write(Fore.RESET)

        ans = _input()
        if strip:
            ans = ans.strip()
        if lower:
            ans = ans.lower()
        elif upper:
            ans = ans.upper()
        elif title:
            ans = ans.title()
        return ans

    def _ask_until(self, question, condition, default=None, color=None,
                   error_msg=None, coerce=None, **kwargs):
        '''
        Asks the user a question until a condition.

        :param question: the question to ask
        :param condition: the callable condition
        :param error_msg: the error message to print on failure
        :param coerce: the callable that returns the coerced value (int, etc)
        :param default: a default value, or None
        :param color: the question text color
        :param strip: whether to strip leading and trailing whitespace
        :param lower: lowercase the result
        :param upper: uppercase the result
        :param title: Title Case The Result
        :return: the inputted text
        '''
        if not callable(condition):
            raise ValueError('condition must be callable')
        if coerce is not None and not callable(coerce):
            raise ValueError('coerce must be callable')
        while True:
            ans = self._ask(question, default=default, color=color, **kwargs)
            if default is not None and not ans:
                ans = default
            try:
                if condition(ans):
                    if coerce:
                        return coerce(ans)
                    return ans
            except:
                pass
            if error_msg:
                print('{}{}{}'.format(Fore.RED, error_msg, Fore.RESET))

    def ask_str(self, question, strip=True, lower=False, upper=False,
                title=False, default=None, color=None):
        '''
        Asks the user a question and expects a string.

        :param question: the question to ask
        :param strip: whether to strip leading and trailing whitespace
        :param lower: lowercase the result
        :param upper: uppercase the result
        :param title: Title Case The Result
        :param default: a default value, or no default at all by default
        :param color: the question text color
        :return: the inputted str
        '''
        ans = self._ask(question, default=default, color=color, strip=strip,
                        title=title, lower=lower, upper=upper)
        if default is not None and not ans:
            return default
        return ans

    def ask_int(self, question, min=None, max=None, default=None, color=None):
        '''
        Asks the user a question and expects an integer response.

        :param question: the question to ask
        :param min: the minimum integer value, inclusive
        :param max: the maximum integer value, inclusive
        :param default: the default integer value
        :param color: the question text color
        :return: the inputed integer within the constraints
        '''

        if min is not None and max is not None:
            return self._ask_until(question, lambda x: int(x) in range(min,
                                                                       max),
                                   default=default, color=color, coerce=int,
                                   error_msg='Must be within range {}-{}'
                                   .format(min, max))
        if min is not None:
            return self._ask_until(question, lambda x: int(x) >= min,
                                   default=default, color=color, coerce=int,
                                   error_msg='Must be greater than or equal '
                                   'to {}'.format(min))
        if max is not None:
            return self._ask_until(question, lambda x: int(x) <= max,
                                   default=default, color=color, coerce=int,
                                   error_msg='Must be less than or equal to '
                                   '{}'.format(max))
        return self._ask_until(question, lambda x: x,
                               default=default, color=color, coerce=int,
                               error_msg='Must be an integer')

    def ask_float(self, question, min=None, max=None, default=None, color=None):
        '''
        Asks the user a question and expects a floating point response.

        :param question: the question to ask
        :param min: the minimum float value, inclusive
        :param max: the maximum float value, inclusive
        :param default: the default float value
        :param color: the question text color
        :return: the inputed float within the constraints
        '''
        if min is not None and max is not None:
            return self._ask_until(question, lambda x: x in range(min, max),
                                   default=default, color=color, coerce=float,
                                   error_msg='Must be within range {}-{}'
                                   .format(min, max))
        if min is not None:
            return self._ask_until(question, lambda x: x >= min,
                                   default=default, color=color, coerce=float,
                                   error_msg='Must be greater than or equal '
                                   'to {}'.format(min))
        if max is not None:
            return self._ask_until(question, lambda x: x <= max,
                                   default=default, color=color, coerce=float,
                                   error_msg='Must be less than or equal to '
                                   '{}'.format(max))
        return self._ask_until(question, lambda x: x,
                               default=default, color=color, coerce=float,
                               error_msg='Must be a floating point')

    def ask_bool(self, question, default=None, color=None):
        '''
        Asks the user a yes/no question.

        :param question: the question to ask
        :param default: the default value, either True or False or None for no
            default
        :param color: the question text color
        :return: either True or False
        '''
        def condition(val):
            if default in (True, False):
                return True
            return bool(val)

        def coerce(val):
            val = val.lower().strip()
            if val in ('true', 'yes', 'y'):
                return True
            elif val in ('false', 'no', 'n'):
                return False
            elif default in (True, False) and not val:
                return default
            else:
                # causes it to error and re-ask
                raise ValueError()

        if default is True:
            prompt = '[Yn]'
        elif default is False:
            prompt = '[yN]'
        else:
            prompt = '[yn]'

        long_prompt = '{}{}'.format(prompt, (self.prompt or ''))

        return self._ask_until(question, condition, default=None,
                               color=color, coerce=coerce, prompt=long_prompt,
                               error_msg='Must be {}'.format(prompt))

    def ask_path(self, question, exists=None, creatable=None, readable=None,
                 writeable=None, is_file=None, is_dir=None, default=None,
                 color=None):
        '''
        Asks the user for a file or directory path.

        :param question: the question to ask
        :param exists: whether or not the path should exist
        :param creatable: whether or not the user should be able to create it
        :param writeable: whether or not the user should be able to write to it
        :param is_file: whether or not the path should be an existing file
        :param is_dir: whether or not the path should be an existing directory
        :param default: the default value, or None for no defaults
        :param color: the question text color
        :return: a path
        '''
        def condition(val):
            val = val.strip()
            if not val and default:
                val = default
            val = os.path.expanduser(val)

            if exists is False and os.path.exists(val):
                return False
            elif exists is True and not os.path.exists(val):
                return False

            dirname = os.path.dirname(val) or os.getcwd()
            if creatable is True and not os.access(dirname, os.W_OK):
                return False
            elif creatable is False and os.access(dirname, os.W_OK):
                return False

            if readable is True and not os.access(val, os.R_OK):
                return False
            elif readable is False and os.access(val, os.R_OK):
                return False

            if writeable is True and not os.access(val, os.W_OK):
                return False
            elif writeable is False and os.access(val, os.W_OK):
                return False

            if is_file is True and not os.path.isfile(val):
                return False
            elif is_file is False and os.path.isfile(val):
                return False

            if is_dir is True and not os.path.isdir(val):
                return False
            elif is_dir is False and os.path.isdir(val):
                return False

            return True

        deps = []
        for msg, cond in (
            ('already exist', exists),
            ('be creatable', creatable),
            ('be readable', readable),
            ('be writeable', writeable),
            ('be a file', is_file),
            ('be a directory', is_dir),
        ):
            if cond is not None:
                if cond:
                    deps.append(msg)
                else:
                    deps.append('not {}'.format(msg))
        if len(deps) > 1:
            last = deps.pop()
            last = 'and {}'.format(last)
            deps.append(last)
        deps = ', '.join(deps)
        error_msg = 'The path must {}'.format(deps)

        return self._ask_until(question, condition, default=default,
                               color=color, error_msg=error_msg)

    def exit(self, message=None, color='red'):
        sys.exit(self._colored(message, color))

    def print(self, message, color=None):
        color = color or self.color
        if color:
            print(self._colored(message, color))
        else:
            print(message)
