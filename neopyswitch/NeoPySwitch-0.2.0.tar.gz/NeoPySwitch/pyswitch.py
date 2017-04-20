"""Python switch-statement pseudo-implementation
Mimics C-style switch statements
The following code blocks should be equivalent
-----------------------------------------------
switch(arg):
    case 1:
        // Handle case
    case 2:
        // Handle case
    default:
        // Handle default case
-----------------------------------------------
@SwitchCase
def case_1(arg1):
    print 'Case 1: ', arg1

@SwitchCase
def case_2(arg1, arg2):
    print 'Case 2: ', arg2

@SwitchCase
def default_case(arg1, arg2, arg3):
    print 'Default case: ', arg1, arg2, arg3

PySwitch(3, {
    1: case_1('a'),
    2: case_2('abc', 42),
    }, default_case(13, 'somestring', 3.14))
"""
__author__ = 'Thomas Li Fredriksen'
__license__ = 'MIT'


def SwitchCase(callable):
    """Switch-case decorator"""
    class case_class(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __call__(self):
            return callable(*self.args, **self.kwargs)

    return case_class


class PySwitch(object):
    def __init__(self, key, cases, default=None):
        """Switch-statement implementation
        :param key: Switch parameter
        :param cases: Dictionary of callbacks
        :param default: Default callback if key is not in cases
        """
        ret = None
        try:
            ret = cases[key]()
        except KeyError:
            if default:
                ret = default()
        finally:
            return ret
