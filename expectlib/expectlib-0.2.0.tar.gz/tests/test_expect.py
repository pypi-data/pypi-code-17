from unittest import TestCase
from expectlib import expect as e


class TestExpect(TestCase):
    def setUp(self):
        from expectlib import Expect
        self.expect = Expect(None)

    def test__equal__returns_equal(self):
        from expectlib.comparison import Equal
        self.assertIsInstance(self.expect.equal(None), Equal)

    def test__not_equal__returns_doesnt_equal(self):
        from expectlib.comparison import DoesntEqual
        self.assertIsInstance(self.expect.not_equal(None), DoesntEqual)


    def test__true__returns_equal(self):
        from expectlib.comparison import Equal
        self.assertIsInstance(self.expect.true(), Equal)

    def test__false__returns_equal(self):
        from expectlib.comparison import Equal
        self.assertIsInstance(self.expect.false(), Equal)

    def test__none__returns_equal(self):
        from expectlib.comparison import Equal
        self.assertIsInstance(self.expect.none(), Equal)

    def test__equal_expression__returns_equal(self):
        from expectlib.comparison import Equal
        self.assertIsInstance((e(10) == 10), Equal)

    def test__greater_than__returns_greater_than(self):
        from expectlib.comparison import GreaterThan
        self.assertIsInstance(self.expect.greater_than(None), GreaterThan)

    def test__not_greater_than__returns_greater_than(self):
        from expectlib.comparison import IsntGreaterThan
        self.assertIsInstance(self.expect.not_greater_than(None), IsntGreaterThan)

    def test__greater_than_expression__returns_greater_than(self):
        from expectlib.comparison import GreaterThan
        self.assertIsInstance((e(10) > 1), GreaterThan)

    def test__lesser_than__returns_lesser_than(self):
        from expectlib.comparison import LesserThan
        self.assertIsInstance(self.expect.lesser_than(None), LesserThan)

    def test__not_lesser_than__returns_lesser_than(self):
        from expectlib.comparison import IsntLesserThan
        self.assertIsInstance(self.expect.not_lesser_than(None), IsntLesserThan)

    def test__lesser_than_expression__returns_lesser_than(self):
        from expectlib.comparison import LesserThan
        self.assertIsInstance((e(10) < 100), LesserThan)

    def test__greater_than_or_equal__returns_greater_than_or_equal(self):
        from expectlib.comparison import GreaterThanOrEqual
        self.assertIsInstance(self.expect.greater_than_or_equal(None), GreaterThanOrEqual)

    def test__not_greater_than_or_equal__returns_greater_than_or_equal(self):
        from expectlib.comparison import IsntGreaterThanOrEqual
        self.assertIsInstance(self.expect.not_greater_than_or_equal(None), IsntGreaterThanOrEqual)

    def test__greater_than_or_equal_expression__returns_greater_than(self):
        from expectlib.comparison import GreaterThanOrEqual
        self.assertIsInstance((e(10) >= 10), GreaterThanOrEqual)

    def test__lesser_than_or_equal__returns_lesser_than_or_equal(self):
        from expectlib.comparison import LesserThanOrEqual
        self.assertIsInstance(self.expect.lesser_than_or_equal(None), LesserThanOrEqual)

    def test__not_lesser_than_or_equal__returns_lesser_than_or_equal(self):
        from expectlib.comparison import IsntLesserThanOrEqual
        self.assertIsInstance(self.expect.not_lesser_than_or_equal(None), IsntLesserThanOrEqual)

    def test__lesser_than_or_equal_expression__returns_lesser_than_or_equal(self):
        from expectlib.comparison import LesserThanOrEqual
        self.assertIsInstance((e(1) <= 10), LesserThanOrEqual)

    def test__contain__returns_contain(self):
        from expectlib.comparison import Contain
        self.assertIsInstance(self.expect.contain(None), Contain)

    def test__not_contain__returns_does_not_contain(self):
        from expectlib.comparison import DoesNotContain
        self.assertIsInstance(self.expect.not_contain(None), DoesNotContain)

    def test__contain_expression__returns_contain(self):
        from expectlib.comparison import Contain
        self.assertIsInstance((e([1, 2, 3]) ^ 2), Contain)

    def test__have__returns_contain(self):
        from expectlib.comparison import Contain
        self.assertIsInstance(self.expect.have(None), Contain)

    def test__not_have__returns_does_not_contain(self):
        from expectlib.comparison import DoesNotContain
        self.assertIsInstance(self.expect.not_have(None), DoesNotContain)

    def test__match__returns_match(self):
        from expectlib.comparison import Match
        self.assertIsInstance(self.expect.match(None), Match)

    def test__not_match__returns_doesnt_match(self):
        from expectlib.comparison import DoesntMatch
        self.assertIsInstance(self.expect.not_match(None), DoesntMatch)

    def test__match_expression__returns_match(self):
        from expectlib.comparison import Match
        self.assertIsInstance((e("foobar") // "^foo"), Match)

    def test__start_with__returns_start_with(self):
        from expectlib.comparison import StartWith
        self.assertIsInstance(self.expect.start_with(None), StartWith)

    def test__not_start_with__returns_start_with(self):
        from expectlib.comparison import DoesntStartWith
        self.assertIsInstance(self.expect.not_start_with(None), DoesntStartWith)

    def test__start_with_expression__returns_start_with(self):
        from expectlib.comparison import StartWith
        self.assertIsInstance((e("foobar") << "foo"), StartWith)

    def test__end_with__returns_end_with(self):
        from expectlib.comparison import EndWith
        self.assertIsInstance(self.expect.end_with(None), EndWith)

    def test__not_end_with__returns_end_with(self):
        from expectlib.comparison import DoesntEndWith
        self.assertIsInstance(self.expect.not_end_with(None), DoesntEndWith)

    def test__end_with_expression__returns_end_with(self):
        from expectlib.comparison import EndWith
        self.assertIsInstance((e("foobar") >> "bar"), EndWith)

    def test__empty__returns_empty(self):
        from expectlib.comparison import Empty
        self.assertIsInstance(self.expect.empty(), Empty)

    def test__not_empty__returns_empty(self):
        from expectlib.comparison import IsntEmpty
        self.assertIsInstance(self.expect.not_empty(), IsntEmpty)

    def test__raises__returns_raises(self):
        from expectlib.comparison import Raises
        self.assertIsInstance(self.expect.raises(None), Raises)

    def test__callable__returns_callable(self):
        from expectlib.comparison import Callable
        self.assertIsInstance(self.expect.callable(), Callable)

    def test__not_callable__returns_callable(self):
        from expectlib.comparison import IsntCallable
        self.assertIsInstance(self.expect.not_callable(), IsntCallable)

    def test__does__returns_instance(self):
        self.assertEqual(self.expect.does, self.expect)

    def test__to__returns_instance(self):
        self.assertEqual(self.expect.to, self.expect)

    def test__be__returns_instance(self):
        self.assertEqual(self.expect.be, self.expect)

    def test__a__returns_instance(self):
        self.assertEqual(self.expect.a, self.expect)

    def test__not__sets_negate_to_true(self):
        self.assertTrue(self.expect._not().negate)

    def test__not_expression__sets_negate_to_true(self):
        self.assertTrue((~e(None)).negate)

    def test__isnt__sets_negate_to_true(self):
        self.assertTrue(self.expect.isnt.negate)

    def test__doesnt__sets_negate_to_true(self):
        self.assertTrue(self.expect.doesnt.negate)
