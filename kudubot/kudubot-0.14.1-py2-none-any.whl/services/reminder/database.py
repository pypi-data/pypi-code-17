u"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

from __future__ import absolute_import
import sqlite3
import logging
from typing import Dict, List
from datetime import datetime
from kudubot.users.Contact import Contact


logger = logging.getLogger(u"kudubot.services.reminder.database")
u"""
The logger for this module
"""


def initialize_database(database):
    u"""
    Initializes the Database Table for the reminder service

    :param database: The database connection to use
    :return: None
    """
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection
    database.execute(u"CREATE TABLE IF NOT EXISTS reminder ("
                     u"    id INTEGER CONSTRAINT constraint_name PRIMARY KEY,"
                     u"    sender_id INTEGER NOT NULL,"
                     u"    msg_text VARCHAR(255) NOT NULL,"
                     u"    due_time VARCHAR(255) NOT NULL,"
                     u"    sent BOOLEAN NOT NULL"
                     u")")
    database.commit()


def convert_datetime_to_string(to_convert):
    u"""
    Converts a datetime object to a string that can be stored in the database

    :param to_convert: The datetime object to convert
    :return: The datetime as a string
    """
    return to_convert.strftime(u"%Y-%m-%d:%H-%M-%S")


def convert_string_to_datetime(to_convert):
    u"""
    Converts a string of the form '%Y-%m-%d:%H-%M-%S' to a datetime object

    :param to_convert: The string to convert
    :return: the resulting datetime object
    """
    return datetime.strptime(to_convert, u"%Y-%m-%d:%H-%M-%S")


def get_next_id(database):
    u"""
    Fetches the next Reminder ID

    :param database: The database to use
    :return: The next highest reminder ID
    """
    # noinspection SqlDialectInspection,SqlNoDataSourceInspection,SqlResolve
    return database.execute(u"SELECT CASE WHEN COUNT(id) > 0 THEN MAX(id) ELSE 0 END AS max_id "
                            u"FROM reminder").fetchall()[0][0] + 1


def store_reminder(database, message, due_time, sender_id):
    u"""
    Stores a reminder in the database

    :param database: The database Connection to use
    :param message: The message text to store
    :param due_time: The time at which the message should be sent
    :param sender_id: The initiator's id in the address book table
    :return: None
    """
    # noinspection SqlNoDataSourceInspection,SqlNoDataSourceInspection,SqlResolve,SqlDialectInspection
    database.execute(u"INSERT INTO reminder (id, sender_id, msg_text, due_time, sent) VALUES (?, ?, ?, ?, ?)",
                     (get_next_id(database), sender_id, message, convert_datetime_to_string(due_time), False))
    database.commit()
    logger.info(u"Reminder stored")


def get_unsent_reminders(database):
    u"""
    Retrieves all unsent reminders from the database

    :param database: The database to use
    :return: A list of dictionaries that contain the reminder information
    """

    # noinspection SqlNoDataSourceInspection,SqlResolve
    results = database.execute(u"SELECT reminder.id, reminder.msg_text, reminder.due_time, address_book.address,"
                               u"       address_book.id, address_book.display_name "
                               u"FROM reminder JOIN address_book ON reminder.sender_id = address_book.id "
                               u"WHERE reminder.sent = 0")
    formatted_results = []
    for result in results:
        formatted_results.append({u"id": result[0],
                                  u"message": result[1],
                                  u"due_time": convert_string_to_datetime(result[2]),
                                  u"receiver": Contact(result[4], result[5], result[3])})
    return formatted_results


def mark_reminder_sent(database, reminder_id):
    u"""
    Marks a reminder as sent

    :param database: The database connection to use
    :param reminder_id: The Reminder ID
    :return: None
    """
    logger.info(u"Marking reminder '" + unicode(reminder_id) + u"' as sent.")
    # noinspection SqlNoDataSourceInspection,SqlResolve
    database.execute(u"UPDATE reminder SET sent=? WHERE id=?", (True, reminder_id))
    database.commit()
