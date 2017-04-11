#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sqlite3_zlib_adapter
----------------------------------

Tests for `sqlite3_zlib_adapter` module.
"""

import sqlite3

import pytest

import sqlite3_zlib_adapter


def test_functional():
    # Register the adapter
    sqlite3.register_adapter(sqlite3_zlib_adapter.ZlibColumn, sqlite3_zlib_adapter.adapt_zlibcolumn)

    # Register the converter
    sqlite3.register_converter("zlibcolumn", sqlite3_zlib_adapter.convert_zlibcolumn)

    z = sqlite3_zlib_adapter.ZlibColumn('value')
    con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("create table test(z zlibcolumn)")

    cur.execute("insert into test(z) values (?)", (z,))
    cur.execute("select z from test")

    res = cur.fetchone()[0]
    assert isinstance(res, sqlite3_zlib_adapter.ZlibColumn)
    assert res == 'value'
    assert str(res) == 'value'
    cur.close()
    con.close()


def test_zlibcolumn_str():
    payload = 'spam'
    z = sqlite3_zlib_adapter.ZlibColumn(payload)
    assert z.payload == payload
    assert z == str(payload)


def test_zlibcolumn_eq():
    payload = 'spam'
    z = sqlite3_zlib_adapter.ZlibColumn(payload)
    assert z == 'spam'


def test_zlibcolumn_constructor():
    payload = 'spam'
    z1 = sqlite3_zlib_adapter.ZlibColumn(payload)
    z2 = sqlite3_zlib_adapter.ZlibColumn.from_compressed(z1.compressed)
    assert z1.payload == z2.payload
    assert z1 == z2


def test_convert_adapter_roundtrip():
    payload = 'spam'
    z = sqlite3_zlib_adapter.ZlibColumn(payload)
    s = sqlite3_zlib_adapter.adapt_zlibcolumn(z)
    z_out = sqlite3_zlib_adapter.convert_zlibcolumn(s)
    assert payload == z_out.payload
