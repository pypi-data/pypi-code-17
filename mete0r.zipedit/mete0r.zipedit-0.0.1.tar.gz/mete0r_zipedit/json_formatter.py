# -*- coding: utf-8 -*-
#
#   mete0r.zipedit: ZipFile editing
#   Copyright (C) 2015-2017 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from functools import wraps
import codecs
import json
import logging


logger = logging.getLogger(__name__)


utf8reader = codecs.getreader('utf-8')
utf8writer = codecs.getwriter('utf-8')


def utf8load(load):
    @wraps(load)
    def wrapper(fp, *args, **kwargs):
        fp = utf8reader(fp)
        return load(fp, *args, **kwargs)
    return wrapper


def utf8dump(dump):
    @wraps(dump)
    def wrapper(o, fp, *args, **kwargs):
        fp = utf8writer(fp)
        return dump(o, fp, *args, **kwargs)
    return wrapper


def utf8loads(loads):
    @wraps(loads)
    def wrapper(b):
        return loads(b.decode('utf-8'))
    return wrapper


def utf8dumps(dumps):
    @wraps(dumps)
    def wrapper(s):
        return dumps(s.encode('utf-8'))
    return wrapper


class JSON(object):
    '''
    JSON formatter interfacing to bytes stream
    '''
    load = staticmethod(utf8load(json.load))
    dump = staticmethod(utf8dump(json.dump))
    loads = staticmethod(utf8loads(json.loads))
    dumps = staticmethod(utf8loads(json.dumps))
