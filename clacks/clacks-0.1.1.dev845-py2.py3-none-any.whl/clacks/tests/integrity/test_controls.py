#!/usr/bin/env python3

"""Test if all PHP Controls have their Python definitions
as well"""

#pylint: disable=no-value-for-parameter

import os


from gtcms.core import fullPath, ROOTPATH
from gtcms.core.db import db
from nose.tools import eq_, assert_in


class TestControls(object):

    """Test if all PHP Controls have their Python definitions
    as well"""

    def setUp(self):
        """Start temporary transaction"""

        from gtcms.models import User
        db.begin_nested()
        user = User()
        user.login = 'test'
        user.password = 'test'
        user.active = True
        db.add(user)
        db.flush()


    def teardown(self):
        """Kill temporary transaction"""
        db.rollback()


    def test_controls_migration(self):
        """tests if all PHP Controls have their Python definitions
        as well"""

        php = {f[:-10] for f in os.listdir(fullPath('include/controls'))
               if f.endswith('.class.php') and f[0] not in '.#'}

        py = {f[:-10] for f in os.listdir(fullPath('lib/gtcms/model'))
              if f.endswith('Control.py') and f[0] not in '.#'}

        eq_(php.difference(py), set())


    def test_controls_locations_list(self):
        """checks if all legacy potential control locations are supported by Python code

        Note: it is perfectly fine for Python to produce locations for more controls than
        PHP code does.
        """
        import requests
        import json
        from gtcms.handlers.ControlsAppendableV1 import ControlsAppendable as CA
        from gtcms.models import ArticleNode, HeadNode

        hn = HeadNode.get()
        page = ArticleNode(title='test', linkName='test', urlPart='test', lang='en')
        page.parent = hn
        db.flush()
        phpresult = json.loads(
            requests.get('http://'+ROOTPATH.name+'/admin_control.php?add={$1}%s'%page.id)
            .content.decode()
        )
        pyresult = CA().default(nodeid=page.id)
        phpresult = sorted(phpresult, key=lambda k: k['id'])

        for phpitem in phpresult:
            assert_in(phpitem['id'], [p['id'] for p in pyresult])
            eq_(phpitem, next((p for p in pyresult if p['id'] == phpitem['id']), None))
