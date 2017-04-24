u"""
LICENSE:
Copyright 2017 Hermann Krumrey

This file is part of kudubot-reminder.

    kudubot-reminder is an extension module for kudubot. It provides
    a Service that can send messages at specified times.

    kudubot-reminder is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot-reminder is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot-reminder.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

from __future__ import absolute_import
import re
import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(u"kudubot_reminder.parsing")


def parse_message(text):
    u"""
    Parses the message and determines the mode of operation

    :param text: The text to parse
    :return: A dictionary with at least the key 'status' with three different possible states:
             - no-match: The message does not match the command syntax
             - help:     A query for the help message. Will result in the help message being sent to the sender
             - store:    Command to store a new reminder
    """

    logger.debug(u"Parsing message")

    text = text.lstrip().rstrip()

    if text.startswith(u"/remind "):  # Due to lstrip rstrip '/remind ' is not a possible message text

        text = text.split(u"/remind ", 1)[1].lstrip().rstrip()

        if re.search(ur' \".+\"$', text) and not text.endswith(u"\\\""):  # Check if message ends in a string

            reminder = text.split(u"\"", 1)[1].rsplit(u"\"", 1)[0]
            usertime = parse_time_string(text.split(u"\"")[0])

            if usertime is None:
                logger.debug(u"Invalid time requirements provided")
                return {u"status": u"no-match"}

            logger.debug(u"Valid reminder syntax. Will store reminder")
            return {u"status": u"store", u"data": {u"message": reminder, u"due_time": usertime}}

        elif text == u"help":
            logger.debug(u"Help message requested")
            return {u"status": u"help"}

        else:
            logger.debug(u"Message does not contain any reminder message")
            return {u"status": u"no-match"}
    else:
        logger.debug(u"Message does not start with '/remind'")
        return {u"status": u"no-match"}


def parse_time_string(time_string):
    u"""
    Parses a time string like '1 week' or '2 weeks 1 day', '2017-01-01' etc. and returns
    a datetime object with the specified time difference to the current time.

    :param time_string: The time string to parse
    :return: The parsed datetime object or None in case the parsing failed
    """
    keywords = {u"today": u"0 day",
                u"tomorrow": u"1 day",
                u"next week": u"1 week",
                u"next year": u"1 year",
                u"days": u"day",
                u"weeks": u"week",
                u"years": u"year",
                u"minutes": u"minute",
                u"seconds": u"second",
                u"hours": u"hour"}

    time_string = time_string.lstrip().rstrip()
    for key in keywords:
        time_string = time_string.replace(key, keywords[key])

    now = datetime.utcnow()

    # Check for absolute time strings
    if re.match(ur'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', time_string):
        date = datetime.strptime(time_string, u"%Y-%m-%d")
        return date.replace(hour=now.hour, minute=now.minute, second=now.second)

    elif re.match(ur'^[0-9]{4}-[0-9]{2}-[0-9]{2}:[0-9]{2}-[0-9]{2}-[0-9]{2}$', time_string):
        return datetime.strptime(time_string, u"%Y-%m-%d:%H-%M-%S")

    elif re.match(ur'^[0-9]{2}-[0-9]{2}-[0-9]{2}$', time_string):
        date = datetime.strptime(time_string, u"%H-%M-%S")
        return date.replace(year=now.year, month=now.month, day=now.day)

    else:

        parsed = time_string.split(u" ")

        if len(parsed) % 2 != 0:
            return None  # Odd number of date keywords are not allowed

        try:
            for i in xrange(0, len(parsed), 2):

                value = int(parsed[i])
                key = parsed[i + 1]

                if key == u"year":
                    now = now.replace(year=now.year + value)
                elif key == u"month":
                    now = now.replace(month=now.month + value)
                elif key == u"day":
                    now = now.replace(day=now.day + value)
                elif key == u"hour":
                    now = now.replace(hour=now.hour + value)
                elif key == u"minute":
                    now = now.replace(minute=now.minute + value)
                elif key == u"second":
                    now = now.replace(second=now.second + value)
                else:
                    logger.debug(u"Invalid time keyword used")
                    return None

            return now

        except ValueError:  # Either integer conversion error or datetime exception
            return None
