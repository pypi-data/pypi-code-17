#!/usr/bin/env python3

""" UserAddress class unit tests """

from nose.tools import eq_, raises


class TestUserAddress(object):

    """ UserAddress class unit tests """

    def setUp(self):
        """ create nested temporary transaction """
        from gtcms.core.db import db
        db.begin_nested()


    def teardown(self):
        """ destroy nested temporary transaction """
        from gtcms.core.db import db
        db.rollback()


    def test_update(self):
        """ tests if update function updated .country attribute """
        from gtcms.core.db import db
        from gtcms.models import UserAddress
        ua = UserAddress(country='Poland')
        db.add(ua)
        db.flush()
        eq_(ua.country, 'Poland')
        ua.update(country='England')
        eq_(ua.country, 'England')


    @raises(ValueError)
    def test_update_id_not_allowed(self):
        """ test if update function forbids .id attribute change """
        from gtcms.core.db import db
        from gtcms.models import UserAddress
        ua = UserAddress(country='Poland')
        db.add(ua)
        db.flush()
        ua.update(id=100)


    def test_update_created_ignored(self):
        """ test if update function ignores .created attribute change """
        from gtcms.core.db import db
        from gtcms.models import UserAddress
        from datetime import datetime
        ua = UserAddress()
        db.add(ua)
        ua.created = '1970-01-01'
        db.flush()
        db.expire_all()
        ua.update(created='1999-12-31')
        eq_(ua.created, datetime(1970, 1, 1))


    def test_export(self):
        """ test if export function returns all data expected """
        from gtcms.core.db import db
        from gtcms.models import UserAddress
        data = {
            'label': 'label1',
            'recipient': 'recipient2',
            'street': 'street3',
            'postcode': 'postcode4',
            'city': 'city5',
            'province': 'province6',
            'country': 'country7',
            'lat': 10,
            'lon': 20}
        ua = UserAddress(**data)
        db.add(ua)
        db.flush()
        data.update({'id': ua.id,
                     'created': str(ua.created)[:19],
                     'tags': None})
        eq_(ua.export(), data)
