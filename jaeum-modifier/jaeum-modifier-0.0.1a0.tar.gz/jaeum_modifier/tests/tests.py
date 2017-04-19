# -*- coding: utf-8 -*-
import unittest

from jaeum_modifier.api import modify, modify_all, modify_by_complexity
from jaeum_modifier.exceptions import (
    InvalidHangulError, InvalidJaeumError, NoComplexityFoundError, NoIndexFoundError
)
from jaeum_modifier.utils import inject_jaeum, replace_eumjul


class TestInterface(unittest.TestCase):

    def test_modify_1(self):
        phrase = u'안녕하세요'
        index = 4
        jaeum = u'ㅎ'
        result = modify(phrase, index, jaeum)
        expected = u'안녕하세효'
        self.assertEqual(result, expected)

    def test_modify_2(self):
        phrase = u'안녕하세요'
        index = -2
        jaeum = u'ㅎ'
        result = modify(phrase, index, jaeum)
        expected = u'안녕하헤요'
        self.assertEqual(result, expected)

    def test_modify_3(self):
        phrase = u'안녕하세요'
        index = 0
        jaeum = u''
        self.assertRaises(InvalidJaeumError, modify, phrase, index, jaeum)

    def test_modify_4(self):
        phrase = u'안녕하세요'
        index = 0
        jaeum = u'B'
        self.assertRaises(InvalidJaeumError, modify, phrase, index, jaeum)

    def test_modify_all_1(self):
        phrase = u'안녕하세요'
        jaeum = u'ㅍ'
        result = modify_all(phrase, jaeum)
        expected = u'판평파페표'
        self.assertEqual(result, expected)

    def test_modify_all_2(self):
        phrase = u'안녕하세요'
        jaeum = u''
        self.assertRaises(InvalidJaeumError, modify_all, phrase, jaeum)

    def test_modify_all_3(self):
        phrase = u'안녕하세요'
        jaeum = u'A'
        self.assertRaises(InvalidJaeumError, modify_all, phrase, jaeum)

    def test_set_by_complexity_1(self):
        phrase = u'안녕하세요'
        jaeum = u'ㅉ'
        complexity = 3
        result = modify_by_complexity(phrase, jaeum, complexity)
        expected = u'짠쪙하세요'
        self.assertEqual(result, expected)

    def test_set_by_complexity_2(self):
        phrase = u'만나서반갑습니다'
        jaeum = u'ㅉ'
        complexity = 2
        result = modify_by_complexity(phrase, jaeum, complexity)
        expected = u'만짜쩌반갑습찌짜'
        self.assertEqual(result, expected)

    def test_set_by_complexity_3(self):
        phrase = u'ㅇㄱㄹㅇ'
        jaeum = u'ㅉ'
        complexity = 1
        result = modify_by_complexity(phrase, jaeum, complexity)
        expected = u'ㅉㅉㅉㅉ'
        self.assertEqual(result, expected)

    def test_set_by_complexity_4(self):
        phrase = u'안녕하세요'
        jaeum = u'ㅉ'
        complexity = -1
        self.assertRaises(NoComplexityFoundError, modify_by_complexity, phrase, jaeum, complexity)


if __name__ == '__main__':
  unittest.main()
