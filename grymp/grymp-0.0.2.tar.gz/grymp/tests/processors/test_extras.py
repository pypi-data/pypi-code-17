# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from grymp.processors.extras import Extras


class TestExtras(unittest.TestCase):

    def test_translate_name_directory(self):
        self.assertEqual(
            Extras._translate_name('A.b.C.d-E.F-Grym'),
            'A b C d - E F')

    def test_translate_name_file(self):
        self.assertEqual(
            Extras._translate_name('Foo.Bar.baz.Bat.(Blim.Blom)-Grym.mkv'),
            'Foo Bar baz Bat (Blim Blom).mkv')

    def test_translate_name_file_blacklist(self):
        self.assertEqual(
            Extras._translate_name('Foo.Bar.720p.TrueHD.Atmos.DD-5.1.(Blim.Blom'
                                   ')-Grym.mkv'),
            'Foo Bar (Blim Blom).mkv')
