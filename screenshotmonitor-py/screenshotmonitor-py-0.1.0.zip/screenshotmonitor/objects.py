# -*- coding: utf-8 -*-
"""

"""

from datetime import datetime

from .api_object import SSMObject
from .exc import NoAssociatedAPIError
from .util import convert_timestamp_to_date, underscore_dict_keys


class Activity(SSMObject):
    def __init__(self, id=None, start=None, end=None, employee=None, offline=None, note=None, project=None):
        super(Activity, self).__init__()
        self.id = id
        self.start = start
        self.end = end
        self.employee = employee
        self.offline = offline
        self.note = note
        self.project = project

    @classmethod
    def from_json_dict(cls, d):
        start = convert_timestamp_to_date(d.get('from'))
        end = convert_timestamp_to_date(d.get('to'))
        activity = cls(id=d.get('id'), start=start, end=end, offline=d.get('offline'),
                       note=d.get('note'), project=d.get('projectId'))
        return activity

    def __str__(self):
        if self.start.date() == self.end.date():
            return "%s from %s to %s" % (self.note, self.start, self.end.time())
        return "%s from %s to %s" % (self.note, self.start, self.end)


class Employee(SSMObject):
    def __init__(self, id=None, name=None, email=None, account_info=None, activity=None, activity_status=None,
                 can_edit=None, config=None, pay_rate=None, projects=None, registered=None, role=None,
                 last_active=None, end_date=None):
        super(Employee, self).__init__()
        self.id = id
        self.name = name
        self.email = email
        self.account_info = account_info
        self.activity = activity
        self.activity_status = activity_status
        self.can_edit = can_edit
        self.config = config
        self.pay_rate = pay_rate
        self.projects = projects
        self.registered = registered
        self.role = role

        self.last_active = convert_timestamp_to_date(last_active)
        self.end_date = convert_timestamp_to_date(end_date)

    @property
    def archived(self):
        return self.end_date is not None

    @archived.setter
    def archived(self, bool):
        if self.archived == bool:
            return  # already in the desired state
        if not self._api:
            raise NoAssociatedAPIError("Employee object is not associated with a ScreenshotMonitor object")
        self._api.set_employee_archived(self, bool)
        self.end_date = datetime.now().timestamp() if bool else None

    def delete(self):
        self._api.delete_employee(self)

    def get_activities(self, start=None, end=None):
        return self._api.get_activities(self, start=start, end=end)

    @classmethod
    def from_json_dict(cls, d):
        # convert camelcase strings to underscored strings
        d = underscore_dict_keys(d)
        d['name'] = d.pop('default_name')

        # convert the dictionaries to Employee objects
        employee = cls(**d)
        return employee

    def __str__(self):
        return "%s: %s%s" % (self.id, self.name, " (archived)" if self.archived else "")
