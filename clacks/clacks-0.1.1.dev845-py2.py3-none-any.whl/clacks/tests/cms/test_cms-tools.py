#!/usr/bin/env python3

"""TestCMSTools test"""

from nose.tools import eq_

from gtcms.core.db import db


class TestCmsTools(object):

    """TestCMSTools test"""

    def setUp(self):
        """ create nested temporary db transaction """
        db.begin_nested()


    def teardown(self):
        """ kill temporary db transaction """
        db.rollback()


    def test_add_language(self):
        """ test if adding language to site  works as expected
        (creates entries in SiteNode and Language collections)
        """
        from gtcms.tools import add_language
        from gtcms.models import SiteNode, Language

        add_language('pl', 'PL')
        pageDB = db.query(SiteNode).filter_by(lang='pl', placement='lang').all()
        eq_(len(pageDB), 1)  # one entry
        eq_(pageDB[0].title, 'polski')
        eq_(pageDB[0].urlPart, 'pl')
        eq_(pageDB[0]._parent, 1)

        langDB = db.query(Language).filter_by(iso_code='pl').one()
        eq_((langDB.name, langDB.native_name, langDB.long_code),
            ('Polish', 'polski', 'pl_PL.UTF-8'))
