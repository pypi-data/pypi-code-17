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

from configdeck.schema import (
    BoolOption,
    Schema,
    Section,
    StringOption,
    )


class NexusSchema(Schema):
    """Configdeck schema for nexus."""

    __version__ = '0.2.3'

    class nexus(Section):
        nexus_media_prefix = StringOption(
            default='/nexus/media/')
        nexus_use_django_media_url = BoolOption(
            default=False)
