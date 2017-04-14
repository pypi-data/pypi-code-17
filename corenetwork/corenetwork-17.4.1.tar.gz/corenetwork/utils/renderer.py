"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.template import loader, Context
import django.conf
from corenetwork.utils.logger import *
from corecluster.utils.exception import CoreException
from logger import log

def render(template_path, context):
    try:
        django.conf.settings.configure({'TEMPLATE_DIRS': (
            '/etc/corecluster/templates/',
            '/etc/corenetwork/drivers/',
        )})
    except:
        pass

    try:
        lv_template = loader.get_template(template_path)
        return lv_template.render(Context(context))
    except Exception as e:
        log(msg="Failed to render template", exception=e, tags=('render', 'error'))
        raise CoreException('template_failed')