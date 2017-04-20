#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.wsgi.cors.cors import cors_filter_factory
from nti.wsgi.cors.cors import cors_option_filter_factory
