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
from dlogg_driver import DLoggDevice
from dlogg_driver.definitions import *
from binascii import hexlify
import MySQLdb as mdb
import time
import logging

log = logging.getLogger(__name__)


class DLoggDbUpload(object):

    CURRENT_DB_FORMAT = 2

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

    def update_tables_format(self):
        version = self.get_format_version()
        while version < DLoggDbUpload.CURRENT_DB_FORMAT:
            self._update_tables_format(version + 1)
            version += 1
        assert self.get_format_version() == DLoggDbUpload.CURRENT_DB_FORMAT

    def insert_current_data(self, data):
        with self._db:
            cur = self._db.cursor()
            self._insert_data(data, cur)
        log.info("Added current data to database")

    # def insert(self, header, data):
    #     with self._db:
    #         cur = self._db.cursor()
    #         self._insert_header(header, cur)
    #         for item in data:
    #             log.debug("Insert data: {}".format(item))
    #             self._insert_data(item, cur)
    #     log.info("Added {} samples to database".format(len(data)))

    def _update_tables_format(self, new_version):
        with self._db:
            cur = self._db.cursor()
            if new_version == 1:
                # create table: internal
                cur.execute('CREATE TABLE internal '
                            '(`key` VARCHAR(255) PRIMARY KEY NOT NULL, `value` TEXT) '
                            'DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin')
                cur.execute("INSERT INTO internal (`key`, `value`) "
                            "VALUES ('version', '1')")
            elif new_version == 2:
                # create table: current_data
                cur.execute('CREATE TABLE current_data ('
                            '`id` INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL, '
                            '`inserted` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                            '`raw` BLOB NOT NULL) '
                            # '`datetime` DATETIME, '
                            # '`timestamp` INTEGER) '
                            'DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin')
                for i in range(0, 16):
                    cur.execute("ALTER TABLE current_data ADD input_{} DOUBLE".format(i + 1))
                    cur.execute("ALTER TABLE current_data ADD input_unit_{} TEXT".format(i + 1))
                for i in range(0, 13):
                    cur.execute("ALTER TABLE current_data ADD output_{} BOOLEAN".format(i + 1))
                for i in range(0, 4):
                    cur.execute("ALTER TABLE current_data ADD pump_speed_{} DOUBLE".format(i + 1))
                    cur.execute("ALTER TABLE current_data ADD pump_speed_unit_{} TEXT".format(i + 1))
            # elif new_version == 3:
            #     # create table: headers
            #     cur.execute('CREATE TABLE headers ('
            #                 '`id` INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL, '
            #                 '`inserted` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, '
            #                 '`raw` BLOB NOT NULL, '
            #                 '`timestamp` INTEGER, '
            #                 '`start` INTEGER, '
            #                 '`end` INTEGER, '
            #                 '`sample_count` INTEGER) '
            #                 'DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin')
            else:
                raise Exception("Unknown format version: {}".format(new_version))
            cur.execute("UPDATE internal SET `value`='{}' WHERE `key`='version'".format(new_version))
            log.info("Database format updated to version {}".format(new_version))

    # @staticmethod
    # def _insert_header(header, cur):
    #     columns = []
    #     values = []
    #     columns.append("raw")
    #     values.append("'{}'".format(hexlify(header.raw)))
    #     columns.append("timestamp")
    #     values.append("'{}'".format(header.timestamp_s))
    #     columns.append("start")
    #     values.append("'{}'".format(header.start.integer))
    #     columns.append("end")
    #     values.append("'{}'".format(header.end.integer))
    #     columns.append("sample_count")
    #     values.append("'{}'".format(header.get_sample_count()))
    #     sql = "INSERT INTO headers ({}) VALUES ({})".format(", ".join(columns), ", ".join(values))
    #     log.debug("SQL: {}".format(sql))
    #     cur.execute(sql)

    @staticmethod
    def _insert_data(data, cur):
        columns = []
        values = []
        columns.append(u"raw")
        values.append(u"'{}'".format(hexlify(data.raw)))
        # dt = data.datetime
        # columns.append("datetime")
        # values.append("'{}-{}-{} {}:{}:{}'".format(dt.year, dt.month, dt.day, dt.hours, dt.minutes, dt.seconds))
        # columns.append("timestamp")
        # values.append("'{}'".format(data.timestamp_s))
        for i in range(0, 16):
            columns.append(u"input_{}".format(i + 1))
            values.append(u"'{}'".format(data.inputs[i].value))
            columns.append(u"input_unit_{}".format(i + 1))
            values.append(u"'{}'".format(data.inputs[i].unit))
        for i in range(0, 13):
            columns.append(u"output_{}".format(i + 1))
            values.append(u"{}".format(data.outputs[i]))
        for i in range(0, 4):
            columns.append(u"pump_speed_{}".format(i + 1))
            values.append(u"'{}'".format(data.pump_speeds[i].value))
            columns.append(u"pump_speed_unit_{}".format(i + 1))
            values.append(u"'{}'".format(data.pump_speeds[i].unit))
        sql = u"INSERT INTO current_data ({}) VALUES ({})".format(u", ".join(columns), u", ".join(values))
        log.debug(u"SQL: {}".format(sql))
        cur.execute(sql)


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

    with DLoggDevice("/dev/ttyUSB0") as device:
        header = device.get_header()
        log.info("Number of samples: {}".format(header.get_sample_count()))
        data = device.fetch_data_range(header.start, 10)
        device.fetch_end()
        with DLoggDbUpload('staging-server', 3306, 'dlogg', 'dlogg', 'dlogg') as upload:
            upload.update_tables_format()
            #upload.insert(header, data)
            for i in range(0, 5):
                upload.insert_current_data(device.get_current_data())
                time.sleep(3.0)
