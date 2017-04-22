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

from configdeck.schema import IntOption, Schema, Section, StringOption


class PyStatsdSchema(Schema):
    """Configdeck schema for pystatsd."""

    __version__ = '0.1.6'

    class statsd(Section):
        statsd_host = StringOption(
            default='localhost')
        statsd_port = IntOption(
            default=8125)
