# -*- coding: utf-8 -*-
"""
    rorocloud.client
    ~~~~~~~~~~~~~~~~

    This module provides the client interface to interact with the
    rorocloud service.

    :copyright: (c) 2017 by rorodata
    :license: Apache 2, see LICENSE for more details.
"""
import sys
import os
from os.path import expanduser, join, exists
import configparser
import requests

config = {
    "ROROCLOUD_URL": "https://rorocloud.rorodata.com/"
}

class Client(object):
    """The rorocloud client.
    """
    def __init__(self, base_url=None):
        self.base_url = base_url or self._get_config("ROROCLOUD_URL")

        self._configfile = join(expanduser("~"), ".rorocloudrc")
        self.auth = self._read_auth()

    def _get_config(self, key):
        return os.getenv(key) or config.get(key)

    def _read_auth(self):
        if not exists(self._configfile):
            return

        p = configparser.ConfigParser(default_section='default')
        p.read(self._configfile)
        try:
            email = p.get("default", "email")
            token = p.get("default", "token")
            return (email, token)
        except configparser.NoOptionError:
            pass

    def _write_auth(self, email, token):
        p = configparser.ConfigParser(default_section='default')
        p.read(self._configfile)
        p.set(None, "email", email)
        p.set(None, "token", token)
        with open(self._configfile, "w") as f:
            p.write(f)
        print("Token saved in", self._configfile)

    def get(self, path):
        url = self.base_url.rstrip("/") + path
        return requests.get(url, auth=self.auth).json()

    def post(self, path, data):
        url = self.base_url.rstrip("/") + path
        return requests.post(url, json=data, auth=self.auth).json()

    def delete(self, path):
        url = self.base_url.rstrip("/") + path
        return requests.delete(url, auth=self.auth).json()

    def jobs(self):
        return [Job(job) for job in self.get("/jobs")]

    def get_job(self, job_id):
        path = "/jobs/" + job_id
        return Job(self.get(path))

    def get_logs(self, job_id):
        path = "/jobs/" + job_id + "/logs"
        return self.get(path)

    def stop_job(self, job_id):
        path = "/jobs/" + job_id
        self.delete(path)

    def run(self, command, shell=False):
        payload = {"command": list(command)}
        data = self.post("/jobs", payload)
        return Job(data)

    def login(self, email, password):
        payload = {"email": email, "password": password}
        data = self.post("/login", payload)
        if "token" in data:
            print("Login successful.")
            self._write_auth(email, data['token'])
        else:
            print("Login failed.", file=sys.stderr)

    def whoami(self):
        return self.get("/whoami")


class Job(object):
    def __init__(self, data):
        self.data = data
        self.id = data['jobid']
        self.status = data['status']
        self.command_args = data['details']['command']
        self.command = " ".join(self.command_args)
        self.status = data["status"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
