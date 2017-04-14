"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import random
import requests
import urllib2
import hashlib
import subprocess
from corenetwork.utils import config
from corenetwork.utils.logger import log


class ApiMixin():
    def _update_state(self, state, comment):
        """
        Update state of node
        """
        log(msg="update_state: setting state to %s" % state, tags=('system', 'info', 'node'))
        auth_seed = hashlib.sha256(str(random.random())).hexdigest()
        self._request('ci/node/update_state/', {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                                'auth_seed': auth_seed,
                                                'state': state,
                                                'comment': comment})


    def _register_node(self):
        """
        Perform node registration (especially, when nod was not added to Core's DB)
        """
        if config.get('node', 'REGISTER'):
            log(msg="register_node: registering node", tags=('system', 'info', 'node'))
            try:
                self._request('ci/node/register/', {'auth_token': config.get('node', 'AUTH_TOKEN'),
                                                    'cpu_total': config.get('node', 'CPU'),
                                                    'memory_total': config.get('node', 'MEMORY'),
                                                    'hdd_total': config.get('node', 'HDD'),
                                                    'username': config.get('node', 'USERNAME')})
            except Exception as e:
                if str(e) != 'node_registered':
                    raise e
        else:
            log(msg="register_node: Registration is disabled", tags=('system', 'info'))


    def _request(self, url, data_dict):
        data = json.dumps(data_dict)
        resp = None

        log(msg='request: %s (%s)' % (url, data), tags=('system', 'info', 'request'))
        for i in xrange(10):
            try:
                resp = requests.post(self._get_core_url() + url, data, timeout=10)
                break
            except requests.exceptions.ConnectionError as e:
                log(msg='request: error: %s' % str(e), tags=('system', 'error', 'request'), exception=e)
                raise Exception('connection_error')
            except requests.exceptions.ConnectTimeout as e:
                log(msg='request: timeout to %s' % url, tags=('system', 'error', 'request'), exception=e)

        if resp is None:
            log(msg='request: empty response', tags=('system', 'info'))
            raise Exception('request_failed')

        try:
            r = json.loads(resp.text)
        except Exception as e:
            log(msg='request: failed to parse response: %s' % resp.text, tags=('system', 'error', 'request'), exception=e)
            raise Exception('unable_to_parse_json')
        if r['status'] != 'ok':
            log(msg='request: returned non ok status: %s' % r['status'], tags=('system', 'error', 'request'))
            raise Exception(r['status'])
        else:
            return r['data']


    def _calc_hash(self, password, hash):
        return hashlib.sha1(password+hash).hexdigest()


    def _get_core_address(self):
        return urllib2.urlparse.urlparse(self._get_core_url()).hostname


    def _get_core_url(self):
        if config.get('network', 'USE_AUTODISCOVER'):
            o = subprocess.check_output('avahi-browse -t -r -p _corecluster_ci._tcp', shell=True)
            for line in o.split('\n'):
                fields = line.split(';')
                if len(fields) > 8 and fields[2] == 'IPv4':
                    url = fields[7]
                    port = fields[8]
                    try:
                        requests.get('https://%s:%s/' % (url, port))
                        return 'https://%s:%s/' % (url, port)
                    except requests.exceptions.ConnectionError as e:
                        return 'http://%s:%s/' % (url, port)

        # If Core was not found via avahi
        core_url = config.get('network', 'CORE_URL')
        if isinstance(core_url, str):
            return core_url
        else:
            if len(core_url) == 0:
                raise Exception('core_url_list_empty')

            for i in xrange(10):
                url = core_url[int(random.random()*len(core_url))]
                try:
                    requests.get(url)
                    return url
                except Exception as e:
                    log(msg='Failed to connect with %s (%d attempt)' % (url, i), tags=('error', 'fatal'), exception=e)
                    continue
            raise Exception('failed_to_connect_ci')
