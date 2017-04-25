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

from .devserver import DevServerSchema
from .django_jenkins import DjangoJenkinsSchema
from .django_openid_auth import DjangoOpenIdAuthSchema
from .nexus import NexusSchema
from .preflight import PreflightSchema
from .pystatsd import PyStatsdSchema
from .raven import RavenSchema
from .saml2idp import Saml2IdpSchema


__all__ = [
    'DevServerSchema',
    'DjangoJenkinsSchema',
    'DjangoOpenIdAuthSchema',
    'NexusSchema',
    'PreflightSchema',
    'PyStatsdSchema',
    'RavenSchema',
    'Saml2IdpSchema',
    ]
