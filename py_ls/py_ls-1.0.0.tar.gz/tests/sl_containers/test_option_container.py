from unittest import TestCase

from py_ls.pattern_matching.pattern_matching import case, _
from py_ls.pattern_matching.pattern_matching import match_f as match
from py_ls.sl_containers.sl_option import Option, Nothing, Some


class TestOption(TestCase):
    def test_should_return_on_nothing(self):
        result = match(Option(None),
                       case > Some, 1,
                       case > Nothing, 2
                       )

        self.assertEqual(result, 2)

    def test_should_handle_nones(self):
        result = match((None, None),
                       case > ("", ""), 1,
                       case > (None, None), 2,
                       case > _, 3
                       )

        self.assertEqual(result, 2)

    def test_should_in_case_of_iterable_check_the_ins(self):
        to_match = (Option(5), Option(1))

        result = match(to_match,
                       case > (Nothing, Nothing), 1,
                       case > (Some, Nothing), 2,
                       case > (Nothing, Some), 3,
                       case > (Some, Some), 4
                       )

        self.assertEqual(result, 4)

        result = match((Nothing, Option(1)),
                       case > (Nothing, Nothing), 1,
                       case > (Some, Nothing), 2,
                       case > (Nothing, Some), 3,
                       case > (Some, Some), 4
                       )

        self.assertEqual(result, 3)

    def test_should_work_with_nothing(self):
        result = match(Option(5),
                       case > Some, 1,
                       case > Nothing, 2
                       )

        self.assertEqual(result, 1)

    def test_should_work_with_lambda(self):
        result = match(Option(5),
                       case > Some, lambda x: x.val,
                       case > Nothing, 2
                       )

        self.assertEqual(result, 5)

    def test_should_work_with_lambda_on_none(self):
        result = match(Option(None),
                       case > Some, lambda x: x,
                       case > Nothing, lambda x: x
                       )

        self.assertEqual(result, Nothing)

    def test_should_return_default_on_get_or_else(self):
        result = Option(None).get_or_else(6)

        self.assertEqual(result, 6)

    def test_should_or_none(self):
        self.assertEqual(Option(None).or_none, None)

    def test_should_raise_on_none(self):
        self.assertRaises(Exception, lambda: Option(None).get)

    def test_should_return_some_on_get(self):
        result = Option(5).get

        self.assertEqual(result, 5)

    def test_should_return_some_on_get_or_else(self):
        result = Option(5).get_or_else(6)

        self.assertEqual(result, 5)

    def test_should_return_is_defined(self):
        result = Option(None).is_defined

        self.assertEqual(result, False)

    def test_should_return_is_empty(self):
        result = Option(None).is_empty

        self.assertEqual(result, True)

    def test_should_for_each(self):
        # when
        class A(object):
            def __init__(self):
                self.val = 0

            def increment(self):
                self.val += 1

        a = A()
        b = A()

        Option(None).foreach(lambda _: a.increment())
        Option(a).foreach(lambda _: a.increment())

        self.assertEqual(a.val, 1)
        self.assertEqual(b.val, 0)

    def test_should_filter_not(self):
        # when
        class A():
            def __init__(self):
                self.val = 0

            def increment(self):
                self.val += 1

        res3 = Option(A()).filter_not(lambda a: a.val != 1).get

        res3.increment()

        self.assertEqual(res3.val, 1)

    def test_should_filter(self):
        # when
        class A():
            def __init__(self):
                self.val = 0

            def increment(self):
                self.val += 1

        res3 = Option(A()).filter(lambda a: a.val == 0).get

        res3.increment()

        self.assertEqual(res3.val, 1)

    def test_should_map(self):
        res2 = Option(5).map(lambda a: a + 1).map(lambda a: a + 1).get

        self.assertEqual(res2, 7)

    def test_should_flat_map(self):
        res2 = Option(5).flat_map(lambda a: Option(a + 1))

        self.assertEqual(res2, Option(6))

    def test_or_else(self):
        res1 = Option(None).or_else(Option(1)).get
        self.assertEqual(res1, 1)

    def test_or_else_2(self):
        res1 = Option(1).or_else(Option(2)).get
        self.assertEqual(res1, 1)

    def test_or_else_raise(self):
        def f():
            return Option(None).or_else_raise(Exception("NO IDEA"))

        self.assertRaises(Exception, f)

    def test_or_else_raise_2(self):
        res1 = Option(1).or_else_raise(Exception("NO IDEA"))
        self.assertEqual(res1, Some(1))

    def test_forall(self):
        self.assertEqual(Option(None).forall(lambda: False), True)

    def test_contains(self):
        self.assertEqual(Option(1).contains(1), True)

    def test_exist(self):
        self.assertEqual(Option(1).exists(lambda x: x < 2), True)

    def test_stringify(self):
        self.assertEqual(str(Option(None)), "Nothing")
        self.assertEqual(str(Nothing), "Nothing")
        self.assertEqual(str(Option(1)), "Some(1)")
        self.assertEqual(str(Some(1)), "Some(1)")

    def test_stringify_2(self):
        self.assertEqual(str([Option(None)]), "[Nothing]")
        self.assertEqual(str([Nothing]), "[Nothing]")
        self.assertEqual(str([Option(1)]), "[Some(1)]")
        self.assertEqual(str([Some(1)]), "[Some(1)]")

    def test_should_collect(self):
        result = Option(5).collect(lambda x: x < 10, lambda x: x * 5)

        self.assertEqual(result, Some(25))

    def test_should_collect_ignore_on_no_predicate(self):
        result = Option(5).collect(lambda x: x > 10, lambda x: x * 5)

        self.assertEqual(result, Nothing)

    def test_should_for_each_2(self):
        # when
        class A(object):
            def __init__(self):
                self.val = 0

            def increment(self):
                self.val += 1

        a = A()
        b = A()

        Option(None).foreach(lambda x: a.increment())
        Option(a).foreach(lambda x: x.increment())

        self.assertEqual(a.val, 1)
        self.assertEqual(b.val, 0)
