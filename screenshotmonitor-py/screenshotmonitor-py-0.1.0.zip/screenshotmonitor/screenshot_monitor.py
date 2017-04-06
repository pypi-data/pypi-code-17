# -*- coding: utf-8 -*-
"""

"""
import re

import six

from .exc import APIError
from .objects import Activity, Employee
from datetime import datetime, timedelta
import requests


class ScreenshotMonitor(object):
    BASE_API_URL = "https://screenshotmonitor.com"

    def __init__(self, xssm_token):
        self.xssm_token = xssm_token
        self._session = requests.Session()
        self._common_data = None
        self._employees_by_id = None
        self.employees = None
        self.refresh()

    def refresh(self):
        """Get the latest employee/company data."""
        self._common_data = self._get_common_data()
        self.employees = self._get_employees_from_common_data(self._common_data)
        self._employees_by_id = {e.id: e for e in self.employees}

    def delete_employee(self, employee):
        endpoint = "/api/v2/DeleteEmployment"
        employee = self._get_employee_object(employee)
        resp = self._post_data(endpoint, json={
            "id": employee.id,
            "archive": False,
            "isPermanentlyDeleted": True
        })
        if resp.status_code != 200:
            raise APIError("%s" % resp.status_code)
        self.employees.remove(employee)
        del self._employees_by_id[employee.id]

    def get_activities(self, employee, start=None, end=None):
        endpoint = "/api/v2/GetActivities"
        employee = self._get_employee_object(employee)
        empid = employee.id
        if end is None:
            end = datetime.now()
        if start is None:
            start = datetime.now() - timedelta(weeks=2)

        resp = self._post_data(endpoint, json=[
            {'employmentId': str(empid), 'from': int(start.timestamp()), 'to': int(end.timestamp())}
        ])
        activities = []
        for actdict in resp.json():  # convert activity JSON dictionaries into Activity objects
            act = Activity.from_json_dict(actdict)
            act._api = self
            act.employee = employee
            activities.append(act)
        return activities

    def get_employee_by_id(self, empid):
        try:
            empid = int(empid)
            assert empid >= 0
        except:
            raise ValueError("Employee ID must be a valid positive integer.")
        return self._employees_by_id[empid]

    def search_employees(self, name_regex, archived=None):
        if isinstance(name_regex, six.string_types):
            name_regex = re.compile(name_regex, re.IGNORECASE)
        matches = []
        for e in self.employees:
            if archived is None or archived == e.archived:
                if name_regex.search(e.name):
                    matches.append(e)
        return matches

    def set_employee_archived(self, employee, bool):
        endpoint = "/api/v2/DeleteEmployment"
        employee = self._get_employee_object(employee)
        resp = self._post_data(endpoint, json={
            "id": employee.id,
            "archive": bool,
            "isPermanentlyDeleted": False
        })
        if resp.status_code != 200:
            raise APIError("%s" % resp.status_code)

    def _get_common_data(self):
        endpoint = "/api/v2/GetCommonData"
        resp = self._get_data(endpoint)
        return resp.json()

    def _get_data(self, endpoint, headers=None):
        url = self.BASE_API_URL + endpoint
        if headers is None:
            headers = {}
        headers.setdefault('X-SSM-Token', self.xssm_token)
        headers.setdefault('Accept', 'application/json')
        response = self._session.get(url, headers=headers)
        return response

    def _get_employee_object(self, employee):
        try:
            empid = int(employee)
            employee = self.get_employee_by_id(empid)
        except TypeError:  # apparently not an integer
            try:
                _ = employee.id
            except AttributeError:
                raise ValueError("Expected an employee ID or an Employee object")
        return employee

    def _post_data(self, endpoint, headers=None, json=None):
        url = self.BASE_API_URL + endpoint
        if headers is None:
            headers = {}
        headers.setdefault('X-SSM-Token', self.xssm_token)
        headers.setdefault('Accept', 'application/json')
        response = self._session.post(url, headers=headers, json=json)
        return response

    def _get_employees_from_common_data(self, data):
        employees = []
        for company in data['companies']:
            employees.extend(company['employments'])
        employees = [Employee.from_json_dict(e) for e in employees]
        for e in employees:
            e._api = self
        return employees


def connect(xssm_token):
    """
    Start ScreenshotMonitor API session. Requires the X-SSM-Token secret. You can obtain it towards
    the bottom of your account page here: https://screenshotmonitor.com/account

    :param xssm_token: the secret value to pass in the X-SSM-Token header
    :return: a ScreenshotMonitor object ready for API calls
    """
    return ScreenshotMonitor(xssm_token)
