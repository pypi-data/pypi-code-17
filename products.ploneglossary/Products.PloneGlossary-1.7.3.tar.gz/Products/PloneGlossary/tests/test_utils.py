# -*- coding: utf-8 -*-
import unittest
from Products.PloneGlossary.utils import html2text
from Products.PloneGlossary.utils import text2words


class UtilsTestCase(unittest.TestCase):

    def test_html2text(self):
        self.assertEqual(html2text('x'), 'x')
        self.assertEqual(html2text('<p class="shiny">text x</p>'), 'text x')
        # Accented character, issue #7.  Well, this does not illustrate the
        # error, as that is in javascript, but it seems nice to test this.
        self.assertEqual(
            html2text('SOMEWORDWITH\xc3\xa8'), 'SOMEWORDWITH\xc3\xa8')
        # '<' and '>' are removed for safety when they are part of a tag:
        self.assertEqual(
            html2text('text <script>alert(42)</script>'),
            'text alert(42)')
        # Actual greater/smaller than signs still work fine:
        self.assertEqual(
            html2text('1 < 2 > 0'),
            '1 < 2 > 0')
        # Well, the actual text that we get when you save the above in a
        # definition actually has escaped tags, which shows fine:
        self.assertEqual(
            html2text('1 &amp;lt; 2'),
            '1 &lt; 2')
        # We are not fooled by dangerous escaped tags:
        self.assertEqual(
            html2text('text &lt;script&gt;alert(42)&lt;/script&gt;'),
            'text scriptalert(42)/script')
        # This may look scary but is actually harmless: it is shown literally
        # in the browser, no alert pops up.
        self.assertEqual(
            html2text('text &amp;lt;script&amp;gt;alert(42)'
                      '&amp;lt;/script&amp;gt;'),
            'text &lt;script&gt;alert(42)&lt;/script&gt;')

    def test_text2words(self):
        self.assertEqual(text2words('x'), ('x',))
        self.assertEqual(text2words('x Y'), ('x', 'Y'))
        self.assertEqual(text2words('foo bar'), ('foo', 'bar'))
        self.assertEqual(text2words('<p>foo bar</p>'), ('foo', 'bar'))
        self.assertEqual(text2words('foo<sub>bar</sub>'), ('foo', 'bar'))
        self.assertEqual(text2words('<p class="shiny">text</p>'), ('text',))
        self.assertEqual(text2words('<p \n>text</\np>'), ('text',))
        self.assertEqual(text2words('<br/>  <br />'), ())
