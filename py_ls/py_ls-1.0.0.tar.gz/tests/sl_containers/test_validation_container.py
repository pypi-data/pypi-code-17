from unittest import TestCase

from py_ls.sl_containers.sl_try import Try
from py_ls.sl_containers.sl_validation import validate, _for_, _yield_
from py_ls.pattern_matching.pattern_matching import match_f as match

class TestSingleValidation(TestCase):
    def test_basic_validation(self):
        x = 10

        result = validate(x,
                          lambda y: y is not None, lambda _: "{} cant be None".format(x),
                          lambda y: y > 10, lambda _: "lower than 10",
                          lambda y: y / 0, lambda _: "not divisable"
                          ) >> _yield_ >> (lambda x: x + 100)

        self.assertEqual(result.get_or_else(123), 123)

        result = validate(x,
                          lambda y: y is not None, lambda _: "{} cant be None".format(x),
                          ) >> _yield_ >> (lambda x: x + 100)

        self.assertEqual(result.get_or_else(123), 110)

    def test_chainable_validation(self):
        x = {
            "test_valid": {
                "start": 1
            }
        }

        result = _for_(x,
                       lambda y: Try(lambda: y["test_valid"]).get_or_else(Try.fail("Can not find 'test_valid' key")),
                       lambda y: Try(lambda: y["start"]).get_or_else(Try.fail("Can not find 'start' key")),
                       lambda y: Try(lambda: int(y)).get_or_else(Try.fail("'Start' key value is not integer"))
                       ) >> _yield_ >> (lambda x: x + 100)

        self.assertEqual(result.get_or_else(11231), 101)
