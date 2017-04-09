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
from common import DLoggDbBase
import pandas as pd
import logging

log = logging.getLogger(__name__)


class DLoggDbDownload(DLoggDbBase):

    def __init__(self, db_host, db_port, db_name, db_user, db_pw):
        DLoggDbBase.__init__(self, db_host, db_port, db_name, db_user, db_pw)

    def fetch_data_range(self, start_utc, end_utc):
        sql = "SELECT * FROM current_data "
        sql += "WHERE inserted >= '{}' AND inserted <= '{}'".format(start_utc, end_utc)
        return pd.read_sql(sql, con=self._db, parse_dates=['inserted'])


if __name__ == "__main__":
    import datetime
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

    with DLoggDbDownload('dlogg-db', 3306, 'dlogg', 'dlogg', 'dlogg') as download:
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=30)
        data = download.fetch_data_range(start, end)
        log.info(u"Data: {}".format(data))
