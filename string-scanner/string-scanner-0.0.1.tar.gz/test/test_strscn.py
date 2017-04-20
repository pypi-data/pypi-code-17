from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from strscan import StringScanner

import pytest


@pytest.fixture
def scanner():
    return StringScanner("bar foobar")


def test_scanner(scanner):
    assert scanner
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match is None


def test_check(scanner):
    assert scanner.check('bar') == 'bar'
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match


def test_check_until(scanner):
    assert scanner.check_until('foo') == 'bar foo'
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match


def test_eos(scanner):
    assert scanner.scan('.*') == 'bar foobar'
    assert scanner.eos() is True


def test_get_byte(scanner):
    assert scanner.get_byte() == 'b'
    assert scanner.pos == 1
    assert scanner.prev_pos == 0
    assert scanner.last_match is None


def test_match(scanner):
    scanner.match('\w+')
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match


def test_peek(scanner):
    assert scanner.peek(2) == "ba"
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match is None


def test_pre_match(scanner):
    scanner.scan('\w+')
    scanner.scan('\s+')
    assert scanner.pre_match() == "bar"


def test_post_match(scanner):
    scanner.scan('\w+')
    scanner.scan('\s+')
    assert scanner.post_match() == "foobar"


def test_reset(scanner):
    scanner.scan('\w+')
    assert scanner.pos == 3
    assert scanner.prev_pos == 0
    assert scanner.last_match
    scanner.reset()
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match is None


def test_rest(scanner):
    scanner.scan('\w+')
    assert scanner.rest() == ' foobar'


def test_scan(scanner):
    assert scanner.scan('\w+') == "bar"
    assert scanner.pos == 3
    assert scanner.prev_pos == 0
    assert scanner.last_match


def test_scan_until(scanner):
    assert scanner.scan_until('foo') == 'bar foo'
    assert scanner.pos == 7
    assert scanner.prev_pos == 0
    assert scanner.last_match


def test_search(scanner):
    scanner.search('\s+')
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match


def test_skip(scanner):
    assert scanner.skip('\w+') == 3
    assert scanner.pos == 3
    assert scanner.prev_pos == 0
    assert scanner.last_match


def test_skip_until(scanner):
    assert scanner.skip_until('foo') == 7
    assert scanner.pos == 7
    assert scanner.prev_pos == 0
    assert scanner.last_match


def test_unscan(scanner):
    scanner.scan('\w+')
    scanner.unscan()
    assert scanner.pos == 0
    assert scanner.prev_pos is None
    assert scanner.last_match

