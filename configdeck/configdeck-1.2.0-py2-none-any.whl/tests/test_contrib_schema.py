# -*- coding: utf-8 -*-
###############################################################################
#
# configdeck -- Stacked configuration sources for your application.
#
# A library for simple, DRY configuration of applications
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
# Copyright © 2009–2013 Canonical Ltd.
#
# This is free software; see the file ‘COPYING’ for details.
#
###############################################################################

from unittest import TestCase

from configdeck.schema import ListOption, StringOption
from configdeck.contrib.schema import DjangoOpenIdAuthSchema


class DjangoOpenIdAuthSchemaTestCase(TestCase):

    def test_openid_launchpad_teams_required_option(self):
        schema = DjangoOpenIdAuthSchema()
        option = schema.openid.openid_launchpad_teams_required
        self.assertTrue(isinstance(option, ListOption))
        self.assertTrue(isinstance(option.item, StringOption))

    def test_openid_email_whitelist_regexp_list_option(self):
        schema = DjangoOpenIdAuthSchema()
        option = schema.openid.openid_email_whitelist_regexp_list
        self.assertTrue(isinstance(option, ListOption))
        self.assertTrue(isinstance(option.item, StringOption))
