import unittest
from unittest import TestCase

from py_ls.constructs.constructs import Raise
from py_ls.pattern_matching.pattern_matching import _, case, f_match_f
from py_ls.pattern_matching.pattern_matching import match as use_match
from py_ls.pattern_matching.pattern_matching import match_f as match


class ThisBase(TestCase):
    def setUp(self):
        self.number = 10
        self.string = "string"

        self.ok = "valid"
        self.bad = "invalid"

        self.list = [1, 2, 3]
        self.set = {1, 2, 3}
        self.dict = {1: 1, 2: 2, 3: 3}

        self.type_int = int


class TestPatternMatching(ThisBase):
    def test_should_raise_exception_on_empty_match_list(self):

        def f():
            x = match(self.number)()

        self.assert_raises_with_message(Exception, "No match found for: {}.".format(self.number), f)

    def test_should_raise_exception_if_value_did_not_match_and_default_was_not_provided(self):
        def f():
            x = match(self.number,
                      case > 1, 10
                      )

        self.assert_raises_with_message(Exception, "No match found for: {}.".format(self.number), f)

    def test_should_not_raise_exception_if_wildcard_was_provided(self):
        x = match(self.number,
                  case > 1, lambda _: self.bad,
                  case > _, lambda _: self.ok
                  )

        self.assertEqual(x, self.ok)

    def assert_raises_with_message(self, exc_class, message, f):
        try:
            f()
            self.fail()
        except Exception as e:
            self.assertTrue(isinstance(e, exc_class))
            self.assertTrue(e.message == message)


class TestPatternMatchingAgainstTypeCases(ThisBase):
    def test_should_match_to_first_correct_type(self):
        x = match(self.number,
                  case > basestring, self.bad,
                  case > int, self.ok,
                  case > Exception, self.bad,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    def test_on_no_match_should_fallback_to_default(self):
        x = match(self.number,
                  case > basestring, self.bad,
                  case > Exception, self.bad,
                  case > _, self.ok
                  )

        self.assertEqual(x, self.ok)

    @unittest.skip("not sure if needed")
    def test_should_support_or(self):
        x = match(self.number,
                  case > basestring, self.bad,
                  case > Or(Exception, int), self.ok,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    @unittest.skip("not sure if needed")
    def test_should_match_types_against_Types(self):
        x = match(self.type_int,
                  case > basestring, self.bad,
                  case > Or(Exception, int), self.ok,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    @unittest.skip("not sure if needed")
    def test_should_support_and(self):
        x = match(self.type_int,
                  case > basestring, self.bad,
                  case > And(int, lambda x: x > 5), self.ok,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

        x = match(4,
                  case > basestring, self.bad,
                  case > And(int, lambda x: x > 5), self.bad,
                  case > And(int, lambda x: x < 5), self.ok,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    @unittest.skip("not sure if needed")
    def test_should_match_types_to_wildcard(self):
        x = match(self.type_int,
                  case > basestring, self.bad,
                  case > Or(Exception, str), self.bad,
                  case > _, self.ok
                  )

        self.assertEqual(x, self.ok)


class TestPatternMatchingAgainstIterableCases(ThisBase):
    def test_should_support_matching_against_list(self):
        x = match(self.list,
                  case > [1, 2], self.bad,
                  case > {1, 2, 3}, self.bad,
                  case > [1, 2, 3], self.ok,
                  case > {1: 1, 2: 2, 3: 3}, self.bad,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    def test_should_in_case_of_iterable_pick_by_type_as_well(self):
        x = match(self.list,
                  case > [1, 2], self.bad,
                  case > list, self.ok,
                  case > [1, 2, 3], self.bad,
                  case > {1: 1, 2: 2, 3: 3}, self.bad,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    def test_should_support_matching_against_set(self):
        x = match(self.set,
                  case > [1, 2], self.bad,
                  case > {1, 2, 3}, self.ok,
                  case > {1: 1, 2: 2, 3: 3}, self.bad,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    def test_should_support_matching_against_dict(self):
        x = match(self.dict,
                  case > [1, 2], self.bad,
                  case > [1, 2, 3], self.bad,
                  case > {1, 2, 3}, self.bad,
                  case > {1: 1, 2: 2, 3: 3}, self.ok,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    @unittest.skip("not sure if needed")
    def test_should_support_wildcard_in_match_expression(self):
        x = match(self.list,
                  case > [1, 2], self.bad,
                  case > [1, 2, _], self.ok,
                  case > {1, 2, 3}, self.bad,
                  case > {1: 1, 2: 2, 3: 3}, self.ok,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    def test_should_not_invoke_callables_on_star_operators(self):
        x = match([],
                  case > [], lambda x: 1,
                  case > _, self.bad
                  )

        self.assertEqual(x, 1)

        x = f_match_f([],
                      case > [], lambda x: x + 1,
                      case > _, self.bad
                      )

        self.assertEqual(x(10), 11)


class CustomClass(object):
    def __init__(self, a):
        self.a = a


class CustomClassDerived(CustomClass):
    pass


class TestPatternMatchingAgainstCustomClasses(ThisBase):
    def test_should_match_custom_types_by_type(self):
        x = match(CustomClass(1),
                  case > 1, self.bad,
                  case > int, self.bad,
                  case > CustomClass, self.ok,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

    def test_should_in_in_case_of_inheritance_go_as_specified(self):
        x = match(CustomClassDerived(1),
                  case > 1, self.bad,
                  case > int, self.bad,
                  case > CustomClass, self.ok,
                  case > CustomClassDerived, self.bad,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)

        x = match(CustomClassDerived(1),
                  case > 1, self.bad,
                  case > int, self.bad,
                  case > CustomClassDerived, self.ok,
                  case > CustomClass, self.bad,
                  case > _, self.bad
                  )

        self.assertEqual(x, self.ok)


class TestPatternMatchingAndSpecialStructures(ThisBase):
    def test_should_support_raising_an_excepion_from_raise_construct(self):
        def f():
            x = match(1,
                      case > [], self.bad,
                      case > [1, 2], self.bad,
                      case > [1, 2, 3], self.bad,
                      case > {1, 2, 3}, self.bad,
                      case > {1: 1, 2: 2, 3: 3}, self.ok,
                      case > _, Raise << Exception("Invalid data")
                      )

        try:
            f()
        except Exception as e:
            self.assertEqual(e.message, "Invalid data")
