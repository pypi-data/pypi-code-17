#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
# Copyright (c) 2015 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aleksandra Tarkowska <A(dot)Tarkowska(at)dundee(dot)ac(dot)uk>, 2008.
#
# Version: 1.0
#
import logging
import warnings
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from omero_version import omero_version

from omeroweb.webclient.decorators import login_required, render_response

logger = logging.getLogger(__name__)


@never_cache
@login_required()
@render_response()
def error404(request, conn=None, **kwargs):
    # it is intentional that this template contains broken links
    context = {"version": omero_version}
    context['template'] = 'weberror/404.html'
    return context


@never_cache
@login_required()
@render_response()
def error500(request, conn=None, **kwargs):
    # it is intentional that this view raise and error
    context['template'] = view_raise_500  # noqa
    return context  # noqa


@never_cache
@render_response()
def warning(request, conn=None, **kwargs):
    warnings.warn("WARN: it is intentional that this view log py.warnings")
    return HttpResponse('Django 1.8+ This view creates warning in a logfile.')
