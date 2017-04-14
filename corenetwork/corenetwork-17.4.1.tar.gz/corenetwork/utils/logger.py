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

import traceback
import syslog
from corenetwork.utils import config
from corenetwork.models import Tag, Message


def _strip_non_ascii(char):
    return char == '\n' or 32 <= ord(char) <= 126


def log(msg=None, context=None, tags=None, exception=None, function=None, agent=None, loglevel='debug'):
    try:
        tag_list = []
        if tags is not None:
            for tag in tags:
                tag_list.append(Tag.get(tag))

        if context is not None:
            if context.user is not None:
                t = Tag.get('user:' + context.user.id)
                if t not in tag_list:
                    tag_list.append(t)

                t = Tag.get('user')
                if t not in tag_list:
                    tag_list.append(t)

            if context.node is not None:
                t = Tag.get('node:' + context.node.id)
                if t not in tag_list:
                    tag_list.append(t)

                t = Tag.get('node')
                if t not in tag_list:
                    tag_list.append(t)

            if context.vm is not None:
                t = Tag.get('vm:' + context.vm.id)
                if t not in tag_list:
                    tag_list.append(t)

                t = Tag.get('vm')
                if t not in tag_list:
                    tag_list.append(t)

        if agent is not None:
            t = Tag.get('agent:' + context.vm.id)
            if t not in tag_list:
                tag_list.append(t)

            t = Tag.get('agent')
            if t not in tag_list:
                tag_list.append(t)

        ll = Tag.get(loglevel)
        if not ll in tag_list:
            tag_list.append(ll)

        log = Message()
        log.message = filter(_strip_non_ascii, msg)

        if exception is not None:
            log.exception = filter(_strip_non_ascii, traceback.format_exc())
            
        try:
            log.installation_id = config.get('node', 'INSTALLATION_ID')
        except:
            log.installation_id = config.get('core', 'INSTALLATION_ID')

        if function is None:
            log.function = traceback.extract_stack(limit=5)[-3][2]
        else:
            log.function = function

        log.save()

        for tag in tag_list:
            log.tags.add(tag)
        log.save()
    except:
        syslog.syslog(syslog.LOG_ERR, 'Failed to log. %s' % msg)
