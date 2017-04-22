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

from configdeck.schema import Section, Schema, StringOption


class PreflightSchema(Schema):
    """Configdeck schema for django-preflight."""

    __version__ = '0.1'

    class preflight(Section):
        preflight_base_template = StringOption(
            default='index.1col.html')
        preflight_table_class = StringOption(
            default='listing')
