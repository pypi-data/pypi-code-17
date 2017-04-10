#!/usr/bin/env python3

"""PageNode class tests"""

from nose.tools import eq_


class TestPageNode(object):

    """PageNode class tests"""

    def setUp(self):
        """Begin temporary transaction"""
        from gtcms.core.db import db
        db.begin_nested()


    def teardown(self):
        """Rollback temporary transaction"""
        from gtcms.core.db import db
        db.rollback()


    def test_PageNode_canonicalize_urlPart(self):
        """Test basic url transliteration."""
        from gtcms.core.db import db
        from gtcms.models import PageNode
        page = PageNode(id=1, linkName='Page 1', title='Page 1', urlPart='ąśćę')
        db.add(page)
        eq_(page.urlPart, 'asce')


    def test_PageNode_parent_switch(self):
        """Test url rewriting if parent page is changed."""
        from gtcms.core.db import db
        from gtcms.models import HeadNode, PageNode
        h = HeadNode.get()
        one = PageNode(linkName='One', title='One', urlPart='one', isBase=True)
        one.parent = h
        eq_(one.url, '/one/')
        two = PageNode(linkName='Two', title='Two', urlPart='two')
        two.parent = one
        eq_(two.url, '/one/two/')
        three = PageNode(linkName='Three', title='Three', urlPart='three', isBase=True)
        three.parent = two
        eq_(three.url, '/one/three/')
        four = PageNode(linkName='Four', title='Four', urlPart='four', isBase=True)
        four.parent = three
        db.flush()
        eq_(four.url, '/one/three/four/')
