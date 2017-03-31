import getpass
import sys
import os.path
import six
from six.moves import configparser
import fire
from terminaltables import AsciiTable
from requests import HTTPError
from .client import CookClient
from .model import *


CONFIG_SECTION = 'cook'


class CookCli(object):
    def __init__(self, base_uri=None, username=None, password=None):
        self._config = configparser.SafeConfigParser({
            'username': getpass.getuser(),
            'password': 'insecure',
            'base_uri': 'http://localhost:12321'
        })
        self._config.read([os.path.expanduser('~/.cookrc')])
        if not self._config.has_section(CONFIG_SECTION):
            self._config.add_section(CONFIG_SECTION)

        if base_uri is None:
            base_uri = self._config.get(CONFIG_SECTION, 'base_uri')
        if username is None:
            username = self._config.get(CONFIG_SECTION, 'username')
        if password is None:
            password = self._config.get(CONFIG_SECTION, 'password')
        self._client = CookClient(base_uri, username, password)

    def run(self, job=None):
        if job is None: # Read from stdin
            job = Job.json_load(sys.stdin)
        elif isinstance(job, six.string_types): # Read from file
                with open(job, 'r') as f:
                    job = Job.json_load(f)
        else:
            job = Job(job)

        try:
            print(self._client.launch(job))
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def status(self, *jobs):
        jobs = list(jobs)
        try:
            statuses = self._client.status(jobs)
            print_jobs(statuses)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def delete(self, *jobs):
        jobs = list(jobs)
        try:
            self._client.delete(jobs)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def retry(self, job, retries):
        try:
            res = self._client.retry_job(job, retries)
            print(res)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def list(self, user, states, start_ms=None, end_ms=None, limit=None):
        try:
            jobs = self._client.list_jobs(user, states, start_ms, end_ms, limit)
            print_jobs(jobs)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))


def print_jobs(jobs):
    for idx, job in enumerate(jobs):
        if idx > 0:
            print("\n\n")
        job = job.get()
        job_table = AsciiTable([
            ['Name', job['name']],
            ['UUID', job['uuid']],
            ['Command', job['command']],
            ['Priority', job['priority']],
            ['Status', job.get('status', '')],
            ['State', job.get('state', '')],
            ['Submit Time', job.get('submit_time', '')],
            ['Retries Remaining', job.get('retries_remaining', '')],
            ['Framework ID', job.get('framework_id', '')],
            ['CPUs', job.get('cpus', '')],
            ['Memory', job.get('mem', '')],
            ['GPUs', job.get('gpus', '')],
            ['User', job.get('user', '')],
            ['Environment', dict_display(job.get('env', dict()))],
            ['Labels', dict_display(job.get('labels', dict()))],
        ], job['name'])
        job_table.inner_heading_row_border = False
        print(job_table.table)

        if 'instances' in job:
            instance_data = [
                ['Status', 'Task ID', 'Hostname', 'Start Time', 'End Time', 'Preempted', 'Reason']
            ]
            for instance in job['instances']:
                # instance = instance.get()
                instance_data.append([
                    instance.get('status', ''),
                    instance.get('task_id', ''),
                    instance.get('hostname', ''),
                    instance.get('start_time', ''),
                    instance.get('end_time', ''),
                    instance.get('preempted', ''),
                    instance.get('reason', '')
                ])
            if len(instance_data) > 1:
                instance_table = AsciiTable(instance_data, '{} Instances'.format(job['name']))
                print("")
                print(instance_table.table)

def dict_display(d):
    return ', '.join(['{}: {}'.format(k, v) for k, v in six.iteritems(d)])

def main():
    fire.Fire(CookCli)

if __name__ == '__main__':
    main()