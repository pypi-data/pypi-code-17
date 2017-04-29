# -*- coding: utf-8 -*-
"""
    rorocloud.client
    ~~~~~~~~~~~~~~~~

    This module provides the client interface to interact with the
    rorocloud service.

    :copyright: (c) 2017 by rorodata
    :license: Apache 2, see LICENSE for more details.
"""
from __future__ import print_function
import sys
import os
from os.path import expanduser, join, exists

try:
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

import requests
from . import __version__
from .utils import logger

config = {
    "ROROCLOUD_URL": "https://rorocloud.rorodata.com/"
}

class Client(object):
    """The rorocloud client.
    """
    USER_AGENT = "rorocloud/{}".format(__version__)
    HEADERS = {
        "User-Agent": USER_AGENT
    }

    def __init__(self, base_url=None):
        self.base_url = base_url or self._get_config("ROROCLOUD_URL")

        self._configfile = join(expanduser("~"), ".rorocloudrc")
        self.auth = self._read_auth()

    def _get_config(self, key):
        return os.getenv(key) or config.get(key)

    def _read_auth(self):
        if not exists(self._configfile):
            return

        p = configparser.ConfigParser()
        p.read(self._configfile)
        try:
            email = p.get("default", "email")
            token = p.get("default", "token")
            return (email, token)
        except configparser.NoOptionError:
            pass

    def _write_auth(self, email, token):
        p = configparser.ConfigParser()
        p.read(self._configfile)

        if not p.has_section("default"):
            p.add_section("default")

        p.set("default", "email", email)
        p.set("default", "token", token)

        with open(self._configfile, "w") as f:
            p.write(f)

        print("Token saved in", self._configfile)

    def _request(self, method, path, **kwargs):
        url = self.base_url.rstrip("/") + path
        try:
            response = requests.request(method, url,
                auth=self.auth,
                headers=self.HEADERS,
                **kwargs)
        except requests.exceptions.ConnectionError:
            logger.error("ERROR: Unable to connect to the rorocloud server.")
            sys.exit(1)

        return response.json()

    def get(self, path):
        return self._request("GET", path)

    def post(self, path, data):
        logger.debug("data %s", data)
        return self._request("POST", path, json=data)

    def delete(self, path):
        return self._request("DELETE", path)

    def jobs(self, all=False):
        if all:
            return [Job(job) for job in self.get("/jobs?all=true")]
        else:
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

    def run(self, command, workdir=None, shell=False):
        details = {}
        if workdir:
            details['workdir'] = workdir
        payload = {"command": list(command), "details": details}
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

    def put_file(self, source, target):
        payload = open(source, 'rb')
        files = { 'file': payload }
        return self._request("POST", "/upload?path="+target, files=files)

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
