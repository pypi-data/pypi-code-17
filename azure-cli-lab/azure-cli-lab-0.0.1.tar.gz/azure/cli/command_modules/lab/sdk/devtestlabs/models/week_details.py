# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class WeekDetails(Model):
    """Properties of a weekly schedule.

    :param weekdays: The days of the week for which the schedule is set (e.g.
     Sunday, Monday, Tuesday, etc.).
    :type weekdays: list of str
    :param time: The time of the day the schedule will occur.
    :type time: str
    """

    _attribute_map = {
        'weekdays': {'key': 'weekdays', 'type': '[str]'},
        'time': {'key': 'time', 'type': 'str'},
    }

    def __init__(self, weekdays=None, time=None):
        self.weekdays = weekdays
        self.time = time
