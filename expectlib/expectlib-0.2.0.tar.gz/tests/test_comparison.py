from unittest import TestCase


class TestEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import Equal
        self.compare = Equal(None, None)

    def test__equal_value__doesnt_raise_error(self):
        self.compare.value = 1
        self.compare.target = 1

        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__matching_bool_target__doesnt_raise_error(self):
        self.compare.value = True
        self.compare.target = True

        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__matching_none_target__doesnt_raise_error(self):
        self.compare.value = None
        self.compare.target = None

        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__nonmatching_bool_target__raises_error(self):
        self.compare.value = False
        self.compare.target = True

        with self.assertRaises(AssertionError):
            self.compare()

    def test__nonmatching_none_target__raises_error(self):
        self.compare.value = 1
        self.compare.target = None

        with self.assertRaises(AssertionError):
            self.compare()

    def test__non_equal_value__raises_error(self):
        self.compare.value = 1
        self.compare.target = 0

        with self.assertRaises(AssertionError):
            self.compare()


class TestGreaterThan(TestCase):
    def setUp(self):
        from expectlib.comparison import GreaterThan
        self.compare = GreaterThan(None, None)

    def test__greater_than_value__doesnt_raise_error(self):
        self.compare.value = 1
        self.compare.target = 0
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.compare.value = 1
        self.compare.target = 1
        with self.assertRaises(AssertionError):
            self.compare()

    def test__lesser_than_value__raises_error(self):
        self.compare.value = 0
        self.compare.target = 1
        with self.assertRaises(AssertionError):
            self.compare()


class TestLesserThan(TestCase):
    def setUp(self):
        from expectlib.comparison import LesserThan
        self.compare = LesserThan(None, None)

    def test__lesser_than_value__doesnt_raise_error(self):
        self.compare.value = 0
        self.compare.target = 1
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.compare.value = 1
        self.compare.target = 1
        with self.assertRaises(AssertionError):
            self.compare()

    def test__greater_than_value__raises_error(self):
        self.compare.value = 1
        self.compare.target = 0
        with self.assertRaises(AssertionError):
            self.compare()


class TestGreaterThanOrEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import GreaterThanOrEqual
        self.compare = GreaterThanOrEqual(None, None)

    def test__greater_than_value__doesnt_raise_error(self):
        self.compare.value = 1
        self.compare.target = 0
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__doesnt_raise_error(self):
        self.compare.value = 1
        self.compare.target = 1
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__lesser_than_value__raises_error(self):
        self.compare.value = 0
        self.compare.target = 1
        with self.assertRaises(AssertionError):
            self.compare()


class TestLesserThanOrEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import LesserThanOrEqual

        self.compare = LesserThanOrEqual(100, 100)

    def test__lesser_than_value__doesnt_raise_error(self):
        self.compare.value = 0
        self.compare.target = 1
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__doesnt_raise_error(self):
        self.compare.value = 1
        self.compare.target = 1
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__greater_than_value__raises_error(self):
        self.compare.value = 1
        self.compare.target = 0
        with self.assertRaises(AssertionError):
            self.compare()


class TestContain(TestCase):
    def setUp(self):
        from expectlib.comparison import Contain
        self.compare = Contain(None, None)

    def test__does_contain_value__doesnt_raise_error(self):
        self.compare.value = [1, 2, 3]
        self.compare.target = 3
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__does_not_contain_value__raises_error(self):
        self.compare.value = [1, 2, 3]
        self.compare.target = 4
        with self.assertRaises(AssertionError):
            self.compare()


class TestMatch(TestCase):
    def setUp(self):
        from expectlib.comparison import Match
        self.compare = Match(None, None)

    def test__matching_value__doesnt_raise_error(self):
        self.compare.value = "foobar"
        self.compare.target = "^foo"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__non_matching_value__raises_error(self):
        self.compare.value = "foobar"
        self.compare.target = "^bar"
        with self.assertRaises(AssertionError):
            self.compare()


class TestStartWith(TestCase):
    def setUp(self):
        from expectlib.comparison import StartWith
        self.compare = StartWith(None, None)

    def test__starts_with_value__doesnt_raise_error(self):
        self.compare.value = "foobar"
        self.compare.target = "foo"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__doesnt_start_with_value__raises_error(self):
        self.compare.value = "foobar"
        self.compare.target = "bar"
        with self.assertRaises(AssertionError):
            self.compare()


class TestEndWith(TestCase):
    def setUp(self):
        from expectlib.comparison import EndWith
        self.compare = EndWith(None, None)

    def test__ends_with_value__doesnt_raise_error(self):
        self.compare.value = "foobar"
        self.compare.target = "bar"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__doesnt_end_with_value__raises_error(self):
        self.compare.value = "foobar"
        self.compare.target = "foo"
        with self.assertRaises(AssertionError):
            self.compare()

class TestDoesntEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntEqual
        self.compare = DoesntEqual(None, None)

    def test__non_equal_value__doesnt_raise_error(self):
        self.compare.value = 1
        self.compare.target = "foo"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.compare.value = 1
        self.compare.target = 1
        with self.assertRaises(AssertionError):
            self.compare()


class TestDoesNotContain(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesNotContain
        self.compare = DoesNotContain(None, None)

    def test__doesnt_contain_value__doesnt_raise_error(self):
        self.compare.value = [1, 2, 3]
        self.compare.target = 4
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__does_contain_value__raises_error(self):
        self.compare.value = [1, 2, 3]
        self.compare.target = 3
        with self.assertRaises(AssertionError):
            self.compare()


class TestDoesntMatch(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntMatch
        self.compare = DoesntMatch(None, None)

    def test__non_matching_value__doesnt_raise_error(self):
        self.compare.value = "foobar"
        self.compare.target = "^bar"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__matching_value__raises_error(self):
        self.compare.value = "foobar"
        self.compare.target = "^foo"
        with self.assertRaises(AssertionError):
            self.compare()


class TestDoesntStartWith(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntStartWith
        self.compare = DoesntStartWith(None, None)

    def test__doesnt_start_with_value__doesnt_raise_error(self):
        self.compare.value = "foobar"
        self.compare.target = "bar"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__starts_with_value__raises_error(self):
        self.compare.value = "foobar"
        self.compare.target = "foo"
        with self.assertRaises(AssertionError):
            self.compare()


class TestDoesntEndWith(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntEndWith
        self.compare = DoesntEndWith(None, None)

    def test__doesnt_with_end_value__doesnt_raise_error(self):
        self.compare.value = "foobar"
        self.compare.target = "foo"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__ends_with_value__raises_error(self):
        self.compare.value = "foobar"
        self.compare.target = "bar"
        with self.assertRaises(AssertionError):
            self.compare()


class TestEmpty(TestCase):
    def setUp(self):
        from expectlib.comparison import Empty
        self.compare = Empty(None)

    def test__empty_list__doesnt_raise_error(self):
        self.compare.value = []
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__empty_tuple__doesnt_raise_error(self):
        self.compare.value = ()
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__none__doesnt_raise_error(self):
        self.compare.value = None
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__non_empty_list__raises_error(self):
        self.compare.value = [1]
        with self.assertRaises(AssertionError):
            self.compare()

    def test__non_empty_string__raises_error(self):
        self.compare.value = "Non empty string"
        with self.assertRaises(AssertionError):
            self.compare()

    def test__non_empty_tuple__raises_error(self):
        self.compare.value = (1,)
        with self.assertRaises(AssertionError):
            self.compare()


class TestIsntEmpty(TestCase):
    def setUp(self):
        from expectlib.comparison import IsntEmpty
        self.compare = IsntEmpty(None)

    def test__empty_list__raises_error(self):
        self.compare.value = []
        with self.assertRaises(AssertionError):
            self.compare()

    def test__empty_tuple__raises_error(self):
        self.compare.value = ()
        with self.assertRaises(AssertionError):
            self.compare()

    def test__none__raises_error(self):
        self.compare.value = None
        with self.assertRaises(AssertionError):
            self.compare()

    def test__non_empty_list__doesnt_raise_error(self):
        self.compare.value = [1]
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__non_empty_string__doesnt_raise_error(self):
        self.compare.value = "Non empty string"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__non_empty_tuple__doesnt_raise_error(self):
        self.compare.value = (1,)
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)


class TestRaises(TestCase):
    def setUp(self):
        from expectlib.comparison import Raises
        self.compare = Raises(None, None)

    def test__error_raising_function_value__doesnt_raise_error(self):
        def fn():
            raise RuntimeError()

        self.compare.value = fn
        self.compare.target = RuntimeError
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__non_error_raising_function_value__raises_error(self):
        def fn():
            pass

        self.compare.value = fn
        self.compare.target = RuntimeError
        with self.assertRaises(AssertionError):
            self.compare()


class TestCallable(TestCase):
    def setUp(self):
        from expectlib.comparison import Callable
        self.compare = Callable(None, None)

    def test__callable_value__doesnt_raise_error(self):
        self.compare.value = lambda: None
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)

    def test__non_callable_value__raises_error(self):
        self.compare.value = "foobar"
        with self.assertRaises(AssertionError):
            self.compare()

class TestIsntCallable(TestCase):
    def setUp(self):
        from expectlib.comparison import IsntCallable
        self.compare = IsntCallable(None, None)

    def test__callable_value__raises_error(self):
        self.compare.value = lambda: None
        with self.assertRaises(AssertionError):
            self.compare()

    def test__non_callable_value__doesnt_raise_error(self):
        self.compare.value = "foobar"
        try:
            self.compare()
        except AssertionError as e:
            self.fail(e)
