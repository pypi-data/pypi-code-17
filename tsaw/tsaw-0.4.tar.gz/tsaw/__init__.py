#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  __init__.py
#
#  Copyright 2017 Yec'han Laizet <y.laizet@bordeaux.unicancer.fr>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


"""
TSAW Torrent Server API Wrapper.

http://ion-torrent-sdk.readthedocs.io/en/latest/
"""


import os
import json
import requests
from requests.auth import HTTPBasicAuth


lib_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(lib_path, 'VERSION')) as version_h:
    __version__ = version_h.read().strip()


def version():
    """Get module version."""
    return __version__


class TorrentServerApi(object):
    """Torrent server api wrapper"""

    def __init__(self, api_url, user, pwd):
        """Class initialiser."""
        self.api_url = api_url
        self.user = user
        self.pwd = pwd

    def get(self, service, params={"format": "json", "limit": 20}):
        """Return get request."""
        get_response = requests.get(
            os.path.join(self.api_url, service),
            auth=HTTPBasicAuth(self.user, self.pwd),
            params=params)
        return get_response

    def resource(self, resource, id=None, params={"format": "json", "limit": 20}):
        """Get resource list.

        return metaData and objects as described
        at http://ion-torrent-sdk.readthedocs.io/en/latest/auto_api_ref_index.html
        """
        resource_str = resource
        if id is not None:
            if isinstance(id, list):
                id_str = ";".join([str(i) for i in id])
                resource_str = os.path.join(resource, "set", id_str)
            else:
                id_str = "%s" % str(id)
                resource_str = os.path.join(resource, id_str)
                return json.loads(self.get(resource_str, params).text)
        return json.loads(self.get(resource_str, params).text)

    def experiment(self, id=None, params={"format": "json", "limit": 20}):
        """Get experiment.

        return metaData and objects as described
        at http://ion-torrent-sdk.readthedocs.io/en/v4.4/auto_api_ref_docs/experiment.html
        """
        return self.resource("experiment", id, params)

    def pluginresult(self, id=None, params={"format": "json", "limit": 20}):
        """Get pluginresult.

        return metaData and objects as described
        at http://ion-torrent-sdk.readthedocs.io/en/v4.4/auto_api_ref_docs/pluginresult.html
        """
        return self.resource("pluginresult", id, params)

    def results(self, id=None, params={"format": "json", "limit": 20}):
        """Get results.

        return metaData and objects as described
        t http://ion-torrent-sdk.readthedocs.io/en/v4.4/auto_api_ref_docs/results.html
        """
        return self.resource("results", id, params)

    def filterby(self, obj_list, key, value):
        """Filter by key / value."""
        return [i for i in obj_list if i[key] == value]
