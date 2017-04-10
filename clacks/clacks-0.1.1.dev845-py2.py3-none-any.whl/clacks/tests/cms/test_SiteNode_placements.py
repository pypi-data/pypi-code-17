#!/usr/bin/env python3

"""SiteNode.placement related tests."""

from gtcms.core import cfg
from gtcms.core.db import db
from nose.tools import eq_


class TestSiteNode(object):

    """SiteNode.placement related tests."""

    def setUp(self):
        """Begin temporary transaction."""
        db.begin_nested()
        self._tmp = cfg.get('page', 'placements')
        cfg.set('page',
                "placements", {
                    "head": {
                        "name": "węzeł nadrzędny",
                        "parent-allow": ["^:"],
                        "supports": ["head"]
                    },
                    "lang": {
                        "name": "menu języka",
                        "parent-allow": [":head"],
                        "supports": ["!", "meta"]
                    },
                    "meta": {
                        "name": "szablon wspólny",
                        "parent-allow": [":lang.*"],
                        "supports": ["meta"]
                    },
                    "none": {
                        "name": "brak",
                        "parent-allow": [":lang.*"],
                        "supports": ["!", "meta"]
                    },
                    "menu1": {
                        "name": "1st menu",
                        "parent-allow": [":lang"],
                    },
                    "menu2": {
                        "name": "1st menu",
                        "parent-allow": [":lang", ":lang:menu1"],
                        "supports": ["!", "meta"]
                    }
                })


    def teardown(self):
        """Rollback temporary transaction."""
        cfg.set('page', 'placements', self._tmp)
        db.rollback()


    def test_SiteNode_placements(self):
        """Test different placement variants."""
        from gtcms.models import HeadNode, ArticleNode
        from gtcms.tools import add_language
        head = HeadNode.get()
        eq_(list(head.placements()), ['head'])
        eq_(head.placement, 'head')
        lang = add_language('pl', 'PL')[0]
        print(repr(lang._placementPath()))
        eq_(list(lang.placements()), ['lang'])
        first = ArticleNode(urlPart='first')
        first.parent = lang
        first.placement = 'menu1'
        eq_(set(first.placements()), set(('none', 'menu1', 'menu2')))
        second = ArticleNode(urlPart='second')
        second.parent = first
        second.placement = "menu2"
        eq_(set(second.placements()), set(('none', 'menu2')))
        third = ArticleNode(urlPart='third')
        third.parent = second
        eq_(set(third.placements()), set(('none',)))
        fourth = ArticleNode(urlPart='fourth')
        fourth.parent = lang
        fourth.placement = 'none'
        fifth = ArticleNode(urlPart='fifth')
        fifth.parent = fourth
        eq_(set(fifth.placements()), set(('none',)))
