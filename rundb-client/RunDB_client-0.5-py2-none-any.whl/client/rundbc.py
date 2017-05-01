import collections

import logging
import requests
from http_api_auth import HTTPApiAuth
import dateutil.parser


class RunDbEntry:

    def __init__(self, experiment, facility, run_number, timestamp, run_id, n_files):
        self.n_files = n_files
        self.run_id = run_id
        self.timestamp = dateutil.parser.parse(timestamp)
        self.run_number = run_number
        self.facility = facility
        self.experiment = experiment

    def __repr__(self):
        return "<RunDbEntry run_id: {}, timestamp: {}, run_number: {}, facility: {}, exp: {}, n_files: {}>"\
                .format(self.run_id, self.timestamp, self.run_number, self.facility, self.experiment, self.n_files)

File = collections.namedtuple('RunDbFile', ['host', 'name', 'directory', 'file_type', 'hash'])


class RunDbc:

    def __init__(self, api_key, host):
        self.auth = HTTPApiAuth(api_key)
        self.host = host
        self.logging = logging.getLogger(self.__class__.__name__)

    def search(self, **kwargs):
        payload = {
            "runNrFrom": kwargs.get('run_number'),
            "runNrTo": kwargs.get('run_number'),
            'experiment': kwargs.get('experiment'),
            'facility': kwargs.get('facility')
        }

        if 'start_time' in kwargs:
            payload.update({'start_time': kwargs.get('start_time')})
        if 'stop_time' in kwargs:
            payload.update({'stop_time': kwargs.get('stop_time')})

        self.logging.info("Searching RunDB for {}".format(payload))
        r = self.__post('search', payload)
        results = r.json()['result']

        entries = [RunDbEntry(j.get('experiment'), j.get('facility'),
                           j.get('run_number'), j.get('timestamp'),
                           j.get('run_id'), j.get('n_files'))
                 for j in results]

        entries.sort(key=lambda entry: entry.timestamp, reverse=True)

        return entries

    def add_log_file(self, run_id, path):
        with open(path, "r") as f:
            content = f.read()
            payload = {"log_file": content, "run_id": run_id }
            return self.__post('upload_log_file', payload).json()

    def add_files(self, run_id, files):
        json_files = [{
                'type': f.file_type,
                'host': f.host,
                'directory': f.directory,
                'name': f.name,
                'hash': f.hash
                } for f in files]

        payload = {
            'run_id': run_id,
            'files': json_files
        }
        return self.__post('add_files', payload).json()

    def __post(self, api, payload):
        url = "{}/api/v1/{}".format(self.host, api)
        return requests.post(url, json=payload, auth=self.auth)