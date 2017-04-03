from unittest import TestCase

from py_ls.constructs.constructs import Raise
from py_ls.pattern_matching.pattern_matching import _, case
from py_ls.pattern_matching.pattern_matching import match_f as match
from py_ls.sl_containers.sl_option import Some, Nothing
from py_ls.sl_containers.sl_try import Try, Success, Failure


class TestTry(TestCase):
    def setUp(self):
        self.exc = Exception("Custom error message")

        def m(x):
            if x < 0:
                return x
            else:
                raise self.exc

        self.test_fun = m

    def test_should_raise_on_get_exception(self):
        side_effect = 0

        def m():
            if side_effect < 0:
                return side_effect
            else:
                raise Exception("Custom error message")

        def f():
            return Try(lambda: m()).get()

        self.assertRaises(Exception, f)

    def test_should_get(self):
        side_effect = -1

        def m():
            if side_effect < 0:
                return side_effect
            else:
                raise Exception("Custom error message")

        # when
        side_effect = -1
        result = Try(lambda: m()).get

        # then
        self.assertEqual(result, -1)

    def test_should_work_with_no_args_lambdas(self):
        side_effect = 0

        def m():
            if side_effect < 0:
                return side_effect
            else:
                raise Exception("Custom error message")

        # when
        result = Try(lambda: m())
        side_effect = -1
        result2 = Try(lambda: m())

        # then
        self.assertEqual(result.is_failure, True)
        self.assertEqual(result.is_success, False)

        self.assertEqual(result2.is_success, True)
        self.assertEqual(result2.is_failure, False)

    def test_should_correctly_indicate_failure_and_success(self):
        # when
        result = Try(lambda: self.test_fun(10))
        result2 = Try(lambda: self.test_fun(-1))

        # then
        self.assertEqual(result.is_failure, True)
        self.assertEqual(result.is_success, False)

        self.assertEqual(result2.is_success, True)
        self.assertEqual(result2.is_failure, False)

    def test_should_correctly_get_the_value_on_get_or_else(self):
        # when
        result = Try(lambda: (self.test_fun(1)))
        result2 = Try(lambda: (self.test_fun(-1)))

        self.assertEqual(result.get_or_else(15), 15)
        self.assertEqual(result2.get_or_else(15), -1)

    def test_should_map(self):
        # when
        result = match(Try(lambda: self.test_fun(-10)) \
                       .map(lambda int: int + 5) \
                       .map(lambda int: int + 5),
                       case > Success, 0,
                       case > Failure, Raise << Exception("Could not evaluate")
                       )

        self.assertEqual(result, 0)

    def test_should_hold_exception(self):
        # when
        result = match(Try(lambda: self.test_fun(-10)) \
                       .map(lambda int: int + "Custom error message") \
                       .map(lambda int: int / 0) \
                       .map(lambda int: int + 5),
                       case > Success, _,
                       case > Failure, lambda f: f.val.message
                       )
        self.assertIn("unsupported operand type", result)

    def test_should_for_each(self):
        # when
        class A():
            def __init__(self):
                self.val = 0

            def increment(self):
                self.val += 1

        a = A()
        b = A()

        Try(lambda: self.test_fun(-10)).foreach(lambda _: a.increment())
        Try(lambda: self.test_fun(10)).foreach(lambda _: a.increment())

        self.assertEqual(a.val, 1)
        self.assertEqual(b.val, 0)

    def test_should_filter(self):
        # when
        res1 = Try(lambda: self.test_fun(-10)).filter(lambda a: a > 0)
        res2 = Try(lambda: self.test_fun(10)).filter(lambda a: a == 0)
        res3 = Try(lambda: self.test_fun(-10)).filter(lambda a: a < 0).get

        self.assertTrue(isinstance(res1, Failure))
        self.assertIn("Predicate does not hold", res1.val.message)
        self.assertTrue(isinstance(res2, Failure))
        self.assertIn("Custom error message", res2.val.message)
        self.assertEqual(-10, res3)

    def test_should_not_map_on_exception(self):
        # when
        def f():
            Try(lambda: self.test_fun(10)).flat_map(lambda int: int + 5) >> match >> (
                case > Failure, Raise << Exception("Could not evaluate")
            )

        self.assertRaises(Exception, f)

    def test_should_not_map_on_exception_2(self):
        # when
        def f():
            match(Try(lambda: self.test_fun(10)).flat_map(lambda int: int + 5),
                  case > Failure, Raise << Exception("Could not evaluate")
                  )

        self.assertRaises(Exception, f)

    def test_iterables_should_work_with_wildcard(self):
        def append(a, b):
            if a == "":
                return b
            if b == "":
                return a
            return a + "|" + b

        def append2(a, b):

            return match((a, b),
                         case > ("", _), b,
                         case > (_, ""), a,
                         case > _, a + "|" + b
                         )

        self.assertEqual(append("", ""), append2("", ""))
        self.assertEqual(append("a", ""), append2("a", ""))
        self.assertEqual(append("", "b"), append2("", "b"))
        self.assertEqual(append("a", "b"), append2("a", "b"))

    def test_should_invert_on_failed(self):
        x = Try(lambda: self.test_fun(10)).failed

        self.assertTrue(isinstance(x, Success))
        self.assertEqual(x.get, self.exc)

        x = Try(lambda: self.test_fun(-1)).failed

        self.assertTrue(isinstance(x, Failure))
        self.assertTrue(isinstance(x.val, RuntimeError))

    def test_try_recover(self):
        x = Try(lambda: self.test_fun(-1)) \
            .map(lambda x: self.test_fun(-1)) \
            .get

        self.assertEqual(x, -1)

        x = Try(lambda: self.test_fun(-1)) \
            .map(lambda x: self.test_fun(10)) \
            .recover(lambda e: 10) \
            .map(lambda x: self.test_fun(x)) \
            .recover(lambda exc: 0) \
            .get

        self.assertEqual(x, 0)

        x = Try(lambda: self.test_fun(-1)) \
            .map(lambda x: self.test_fun(-1)) \
            .recover(lambda exc: 0) \
            .get

        self.assertEqual(x, -1)

    def test_to_option(self):
        x = Try(lambda: self.test_fun(-1)) \
            .option

        self.assertEqual(x, Some(-1))

        y = Try(lambda: self.test_fun(10)) \
            .option

        self.assertEqual(y, Nothing)

    def test_transform(self):
        x = match(Try(lambda: self.test_fun(-1)) \
                  .transform(lambda x: Success(x + 1), lambda x: Failure(x.message)),
                  case > Success, lambda s: s.get,
                  case > Failure, lambda s: s.get_exc.message
                  )

        self.assertEqual(x, 0)

        y = match(Try(lambda: self.test_fun(10)) \
                  .transform(lambda x: Success(x + 1), lambda x: Failure(Exception("changed exception"))),
                  case > Success, lambda s: s.get,
                  case > Failure, lambda s: s.get_exc.message,
                  )
        self.assertEqual(y, "changed exception")

    def test_map_flatmap(self):
        y = Try(lambda: 0 / 10) \
            .map(lambda x: Try(lambda: x * 2).map(lambda x: Try(lambda: x * 2)))
        self.assertEqual(str(y), "Success(Success(Success(0)))")

        y = Try(lambda: 0 / 10) \
            .flat_map(lambda x: Try(lambda: x * 2).flat_map(lambda x: Try(lambda: x * 2)))
        self.assertEqual(str(y), "Success(0)")

    def test_should_map_and_flatmap_preserve_exceptions(self):
        y = Try(lambda: 0 / 10) \
            .map(lambda x: x / 0) \
            .map(lambda x: x.meeee)
        self.assertEqual(str(y), "Failure(\"integer division or modulo by zero\")")

        y = Try(lambda: 0 / 10) \
            .flat_map(lambda x: Try(lambda: x / 0)) \
            .flat_map(lambda x: Try(lambda: x.meeee))

        self.assertEqual(str(y), "Failure(\"integer division or modulo by zero\")")

    def test_stringify(self):
        self.assertEqual(str(Try(lambda: self.test_fun(10))), "Failure(\"Custom error message\")")
        self.assertEqual(str(Try(lambda: self.test_fun(-1))), "Success(-1)")

    def test_stringify_2(self):
        self.assertEqual(str([Try(lambda: self.test_fun(10))]), "[Failure(\"Custom error message\")]")
        self.assertEqual(str([Try(lambda: self.test_fun(-1))]), "[Success(-1)]")
