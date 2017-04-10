#!/usr/bin/env python3

"""SiteNode related tests"""

from nose.tools import eq_


class TestSiteNode(object):

    """SiteNode related tests"""

    def setUp(self):
        """Begin temporary transaction"""
        from gtcms.core.db import db
        db.begin_nested()


    def teardown(self):
        """Rollback temporary transaction"""
        from gtcms.core.db import db
        db.rollback()


    def test_SiteNode_hasChildren(self):
        """Children count related test."""
        from gtcms.core.db import db
        from gtcms.models import PageNode, HeadNode
        first = HeadNode.get()
        db.add(first)
        second = PageNode(id=2, linkName='Page 2', title='Page 2', urlPart='other')
        second.parent = first
        db.add(second)
        db.flush()
        eq_(first.childNodesCount, 1)
        eq_(second.childNodesCount, 0)


    def test_copyTo(self):
        """ it needs to be moved to PageNode test and here should be
        other, more general one implemented
        """
        from gtcms.core.db import db
        from gtcms.models import PageNode, HeadNode
        head = HeadNode.get()

        first = PageNode(linkName='Page 1', title='Page 1', urlPart='other')
        first.parent = head
        db.flush()
        second = first.copyTo(head)
        db.flush()
        eq_(first.position, 0)
        eq_(second.position, 1)
        eq_(second.linkName, 'Page 1')
        eq_(second.urlPart, 'other')
        eq_(first.url, '/other/')
        eq_(second.url, '/other-1/')
        eq_(first is second, False)
        db.delete(head.childNodes.pop(1))


    def test_position_normalisation(self):
        """ if position is out of range, it should be normalized """

        from gtcms.core.db import db
        from gtcms.models import PageNode, HeadNode

        head = HeadNode.get()

        first = PageNode(linkName='Page 1', title='Page 1', urlPart='other')
        first.parent = head
        db.flush()
        eq_(first.parent, head)
        #eq_(first.position, 1)

        second = PageNode(linkName='Page 2', title='Page 2', urlPart='other')
        second.parent = head
        eq_(second.parent, head)
        eq_(second.position, 1)

        third = PageNode(linkName='Page 3', title='Page 3', urlPart='other')
        third.parent = head
        eq_(third.parent, head)
        eq_(third.position, 2)
