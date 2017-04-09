#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# python-dlogg-db - Python package to handle data from a D-LOGG device
# Copyright (C) 2017 U. Bruhin
# https://github.com/ubruhin/python-dlogg-db
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import MySQLdb as mdb
import logging

log = logging.getLogger(__name__)


class DLoggDbBase(object):

    def __init__(self, db_host, db_port, db_name, db_user, db_pw):
        self._db = mdb.connect(host=db_host, port=db_port, user=db_user,
                               passwd=db_pw, db=db_name, charset='utf8')
        log.info("Opened database {} on host {}".format(db_name, db_host))
        log.info("Database format version: {}".format(self.get_format_version()))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._db.close()
        log.info("Closed database")

    def get_format_version(self):
        with self._db:
            cur = self._db.cursor()
            cur.execute("SHOW TABLES LIKE 'internal'")
            if cur.fetchone():
                cur.execute("SELECT `value` FROM internal WHERE `key`='version'")
                return int(cur.fetchone()[0])
            else:
                return 0
