# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

""" API Module handles all calls to/from the tCell service. Errors are
handled gracefully since it's generally running silently and should
fail open.
"""

from __future__ import unicode_literals

import json
import logging
import sys
from io import BytesIO

import pycurl

from tcell_agent.config import CONFIGURATION
from tcell_agent.version import VERSION

try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode


LOGGER = logging.getLogger('tcell_agent').getChild(__name__)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

    def encode(self, obj):
        def traverse(obj):
            if isinstance(obj, dict):
                return {k: traverse(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [traverse(elem) for elem in obj]
            elif (isinstance(obj, str) or isinstance(obj, bytes) or (
                    sys.version_info < (3, 0) and isinstance(obj, unicode))) and len(obj) > 256:
                return obj[:256]
            else:
                return obj  # no container, just values (str, int, float)

        return super(SetEncoder, self).encode(traverse(obj))


class TCellAPIException(Exception):
    """Special API Exception"""
    pass


class TCellAPI(object):
    """API Class handling comms"""

    def v1update(self, last_timestamp=None):
        """v1 is the new rest API endpoint"""
        url = '{url}/app/{appname}/update'.format(
            url=CONFIGURATION.tcell_api_url,
            appname=CONFIGURATION.app_id)
        LOGGER.debug("calling api: %s", url)
        response_code = None
        response_buffer = BytesIO()

        try:
            params = {}
            if last_timestamp:
                params["last_timestamp"] = last_timestamp
            headers = ["Authorization: Bearer " + CONFIGURATION.api_key,
                       "TCellAgent: Python " + VERSION,
                       "Accept: application/json"]
            c = pycurl.Curl()
            c.setopt(c.URL, url + '?' + urlencode(params))
            c.setopt(c.WRITEDATA, response_buffer)
            c.setopt(pycurl.HTTPHEADER, headers)
            c.perform()
            response_code = c.getinfo(c.RESPONSE_CODE)
            c.close()

        except Exception as general_exception:
            LOGGER.error("Error connecting to tcell: {e}".format(e=general_exception))
            LOGGER.debug(general_exception, exc_info=True)
            raise TCellAPIException("could not connect to server")

        if response_code == 200:
            try:
                body = response_buffer.getvalue().decode('utf-8')
                LOGGER.debug("response: %s", body)

                response_json = json.loads(body)
                return response_json.get("result", None)
            except Exception as general_exception:
                LOGGER.error("Error parsing tcell response: {e}".format(e=general_exception))
                LOGGER.debug(general_exception, exc_info=True)
                raise TCellAPIException("Result field not found")

        LOGGER.debug("v1update error response code: %s", response_code)
        raise TCellAPIException("Response was not 'ok'")

    def v1send_events(self, events):
        """
        Sends events to tCell via the API
        v1 is the new rest API
        """
        event_endpoint = "server_agent"
        url = '{url}/app/{appname}/{endpoint}'.format(
            url=CONFIGURATION.tcell_input_url,
            appname=CONFIGURATION.app_id,
            endpoint=event_endpoint)
        payload = {"hostname": CONFIGURATION.host_identifier,
                   "uuid": CONFIGURATION.uuid,
                   "events": events}
        LOGGER.debug("sending events to %s", url)
        LOGGER.debug(json.dumps(payload, cls=SetEncoder))
        headers = ["Authorization: Bearer " + CONFIGURATION.api_key,
                   "Content-type: application/json",
                   "TCellAgent: Python " + VERSION,
                   "Accept: application/json"]

        response_buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.POSTFIELDS, json.dumps(payload, cls=SetEncoder))
        c.setopt(c.WRITEDATA, response_buffer)
        c.perform()
        response_code = c.getinfo(c.RESPONSE_CODE)
        c.close()

        body = ""
        if response_code == 200:
            try:
                body = response_buffer.getvalue().decode('utf-8')

            except Exception as general_exception:
                LOGGER.error("Error in send_events response: {e}".format(e=general_exception))
                LOGGER.debug(general_exception, exc_info=True)

        LOGGER.debug("send_events response[%s]: %s", response_code, body)
        return response_code
