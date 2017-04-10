#!/usr/bin/env python3

"""Test if there are any mappers left in config."""

from gtcms.core import cfg
from nose.tools import eq_


class TestOldMappers(object):

    """Test if there are any mappers left in config."""

    def test_old_config(self):
        """Test if any obsolete config entry can be still found."""
        entries = [
            ('controls', 'box_locations'),
            ('controls', 'SearchResults', 'locations'),
            ('controls', 'sitemap', 'locations'),
            ('controls', 'banners', 'locations'),
            ('controls', 'PromotedProducts', 'locations'),
            ('controls', 'PromotedProduct', 'locations'),
            ('controls', 'Gallery', 'locations')
        ]

        for entry in entries:
            eq_(cfg.get(*entry, default=None), None, msg=repr(entry)+" path found in config")
