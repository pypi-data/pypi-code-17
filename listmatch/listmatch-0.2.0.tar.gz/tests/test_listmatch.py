#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_listmatch
----------------------------------

Tests for `listmatch` module.
"""


import unittest

from hamcrest import (
    anything,
    assert_that,
    contains,
    contains_inanyorder,
    is_not
)
from hamcrest.core.base_matcher import BaseMatcher
from listmatch import atom, concat, maybe, one_or_more, options, zero_or_more
from listmatch.util import explain_none, MatchSummary


class ListMatchMatcher(BaseMatcher):
    def __init__(self, list, paths):
        self.list = list
        self.paths = paths
        self.path_matcher = contains_inanyorder(*[
            contains(*path)
            for path in self.paths
        ]) if paths else anything()

    def _matches(self, matcher):
        explain = (self.paths is not None)
        match_info = matcher.match(self.list, explain=explain)
        if explain:
            return (
                match_info.is_match and
                self.path_matcher.matches(
                    match_info.explanation.possibilities
                )
            )
        return match_info.is_match

    def describe_mismatch(self, matcher, mismatch_description):
        matches, paths = matcher.match(self.list)
        if not matches:
            mismatch_description.append_text(self.list) \
                                .append_text(" didn't match")
        else:
            mismatch_description.append_text("paths ")
            self.path_matcher.describe_mismatch(
                paths.possibilities,
                mismatch_description
            )

    def describe_to(self, description):
        description.append_text('matches list ') \
                   .append_text(self.list)
        description.append_text(', and paths matches ') \
                   .append_description_of(self.path_matcher)


def matches(item, paths=None):
    return ListMatchMatcher(item, paths)


@explain_none
def is_a(x):
    return x == 'a'


@explain_none
def is_even(x):
    return x % 2 == 0


def times_2(x, explain):
    return MatchSummary(True, x*2)


class TestListmatch(unittest.TestCase):
    def test_basic(self):
        assert_that(atom(is_a), matches(['a']))
        assert_that(atom(is_a), is_not(matches(['b'])))

        assert_that('a' + atom('b'), matches('ab'))
        assert_that('a' + atom('b'), is_not(matches('a')))

        assert_that(concat(), matches([]))
        assert_that(concat(), is_not(matches('a')))

        assert_that(concat(atom('a')), matches(['a']))

        assert_that(options(), is_not(matches([])))
        assert_that(options(), is_not(matches('a')))

        assert_that(options('a', 'b'), matches(['a']))
        assert_that(options('a', 'b'), is_not(matches(['c'])))

        assert_that(zero_or_more(is_even), matches([]))
        assert_that(zero_or_more(is_even), matches([0, 2, 4]))
        assert_that(zero_or_more(is_even), is_not(matches([0, 3, 4])))

        example = zero_or_more('a') + one_or_more('b' | ('c' + maybe('d')))
        assert_that(example, matches(['a', 'a', 'b', 'c', 'c', 'd']))
        assert_that(example, matches(['b', 'c', 'c', 'd']))
        assert_that(example, matches(['a', 'a', 'b', 'b', 'c', 'c', 'd']))
        assert_that(example, is_not(matches(['a', 'a', 'b', 'b', 'd'])))
        assert_that(example, is_not(matches(['a', 'a'])))

        assert_that(concat(), matches([], paths=[]))
        assert_that(atom(times_2), matches([2], paths=[[4]]))
        assert_that(options(times_2, is_even), matches(
            [2],
            paths=[[4], [None]]
        ))
        assert_that(options(times_2, 3), matches([2], paths=[[4]]))
        assert_that(
            concat(0, options(times_2, is_even)),
            matches([0, 2], paths=[[None, 4], [None, None]])
        )
