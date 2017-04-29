from unittest import TestCase


class TestEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import Equal

        self.eq = Equal(10, 10)

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.value = 100
        with self.assertRaises(AssertionError):
            self.eq()


class TestGreaterThan(TestCase):
    def setUp(self):
        from expectlib.comparison import GreaterThan

        self.eq = GreaterThan(100, 10)

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.value = 10
        with self.assertRaises(AssertionError):
            self.eq()


class TestLesserThan(TestCase):
    def setUp(self):
        from expectlib.comparison import LesserThan

        self.eq = LesserThan(10, 100)

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.value = 1000
        with self.assertRaises(AssertionError):
            self.eq()


class TestGreaterThanOrEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import GreaterThanOrEqual

        self.eq = GreaterThanOrEqual(100, 10)

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.value = 1
        with self.assertRaises(AssertionError):
            self.eq()


class TestLesserThanOrEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import LesserThanOrEqual

        self.eq = LesserThanOrEqual(100, 100)

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__lesser_than_value__doesnt_raise_error(self):
        self.eq.value = 10
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__greater_than_value__raises_error(self):
        self.eq.value = 1000
        with self.assertRaises(AssertionError):
            self.eq()


class TestIs(TestCase):
    def setUp(self):
        from expectlib.comparison import Is

        self.eq = Is(True, True)

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.value = False
        with self.assertRaises(AssertionError):
            self.eq()


class TestContain(TestCase):
    def setUp(self):
        from expectlib.comparison import Contain

        self.eq = Contain([1, 2, 3], 3)

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.target = 4
        with self.assertRaises(AssertionError):
            self.eq()


class TestMatch(TestCase):
    def setUp(self):
        from expectlib.comparison import Match

        self.eq = Match("foobar", "^foo")

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.target = "^bar"
        with self.assertRaises(AssertionError):
            self.eq()


class TestStartWith(TestCase):
    def setUp(self):
        from expectlib.comparison import StartWith

        self.eq = StartWith("foobar", "foo")

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.target = "bar"
        with self.assertRaises(AssertionError):
            self.eq()


class TestEndWith(TestCase):
    def setUp(self):
        from expectlib.comparison import EndWith

        self.eq = EndWith("foobar", "bar")

    def test__equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__non_equal_value__raises_error(self):
        self.eq.target = "foo"
        with self.assertRaises(AssertionError):
            self.eq()

class TestDoesntEqual(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntEqual

        self.eq = DoesntEqual(10, 100)

    def test__non_equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.eq.target = 10
        with self.assertRaises(AssertionError):
            self.eq()


class TestIsnt(TestCase):
    def setUp(self):
        from expectlib.comparison import Isnt

        self.eq = Isnt(True, False)

    def test__non_equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.eq.target = True
        with self.assertRaises(AssertionError):
            self.eq()


class TestDoesNotContain(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesNotContain

        self.eq = DoesNotContain([1, 2, 3], 4)

    def test__non_equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.eq.target = 3
        with self.assertRaises(AssertionError):
            self.eq()


class TestDoesntMatch(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntMatch

        self.eq = DoesntMatch("foobar", "^bar")

    def test__non_equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.eq.target = "^foo"
        with self.assertRaises(AssertionError):
            self.eq()


class TestDoesntStartWith(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntStartWith

        self.eq = DoesntStartWith("foobar", "bar")

    def test__non_equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.eq.target = "foo"
        with self.assertRaises(AssertionError):
            self.eq()


class DoesntEndWith(TestCase):
    def setUp(self):
        from expectlib.comparison import DoesntEndWith

        self.eq = DoesntEndWith("foobar", "foo")

    def test__non_equal_value__doesnt_raise_error(self):
        try:
            self.eq()
        except AssertionError as e:
            self.fail(e)

    def test__equal_value__raises_error(self):
        self.eq.target = "bar"
        with self.assertRaises(AssertionError):
            self.eq()
