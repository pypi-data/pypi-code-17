#!/usr/bin/env python3

"""Page factories related tests."""

from gtcms.core import cfg
from nose.tools import eq_


class TestPageFactories(object):

    """Page factories related tests."""

    def test_factory_compatibility(self):
        """Check whether there's any PHP page type that doesn't
        have its Python factory equivalent.
        """
        old = set(cfg.get('admin', 'page_types', default={}).keys())
        new = set(cfg.get('page', 'factory').keys())
        eq_(old.issubset(new), True,
            "Factory not found for old page_types: %r" % old.difference(new))
