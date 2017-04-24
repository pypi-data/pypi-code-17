import getpass
import sys
import os.path
import six
from six.moves import configparser
from docopt import docopt
from terminaltables import AsciiTable
from requests import HTTPError
from .client import CookClient
from .model import *
from .logs import FileFetcher
from . import __version__


CONFIG_SECTION = 'cook'


__doc__ = """Cook

Note: The Cook scheduler is intended to be used by applications that track their own job UUIDs and submit large
      numbers of jobs programmatically. Managing jobs through a CLI might always be a bit of a hack.

Usage:
    cook [options] run (--json=<json> | --file=<json-file> | -)
    cook [options] status <job-uuid>...
    cook [options] delete <job-uuid>...
    cook [options] retry <job-uuid> <retries>
    cook [options] list <user> <states> [<limit> <start_ms> <end_ms>]
    cook [options] logs <job-uuid> (--stdout | --stderr)
    cook (-h | --help)

Options:
    -b --base_uri <base-uri>  URI of Cook server
    -u --username <username>  Cook username
    -p --password <password>  Cook password

Commands:
    run     Run a job. Job descriptions can be given on stdin, passed as a string argument
            with --json, or from a file with --file
    status  Display the status and running instances of a job or jobs
    delete  Delete a job or jobs
    retry   Retry a job some number of times
    list    List jobs matching the given conditions
            <states> can be any of 'waiting', 'running', or 'completed', joined with a '+'
    logs    Display stdout or stderr for a job

Job Descriptions:
    Job descriptions are JSON objects of the following form (see mesos_cook.models.Job) for more information

    {
        "name": "my-job", // required
        "uuid": "8E86A336-58AD-43D9-A9DC-566D74536FF4" // required, must be unique since it's used to identify the job in other commands
        "priority": 50, // required, from 1 to 100 inclusive
        "command": "rm -rf /", // required command string
        "max_retries": 3, // required, how many times to retry the job if it fails
        "max_runtime": 1000, // optional, how long (in milliseconds) the job is allowed to run for
        "cpus": 1.5, // required, how many CPU shares to allocate
        "mem": 128.0, // required, how much memory (in MiB) to allocate
        "gpus": 3, // optional, how many GPUs to allocate. Cook won't schedule non-GPU jobs on GPU nodes, so if all nodes have GPUs, then all jobs must request GPUs to be scheduled
        "ports": 1, // optional, how many ports to be opened for the job (will be passed to the job in environment variables)
        "container": { // optional container description
            "type": "MESOS", // required, either MESOS or DOCKER
            "docker": { // Docker info. The image name is used by the Mesos containerizer as well
                "image": "nvidia/cuda:8.0", // Docker image to use
                "force_pull_image": false, // Whether or not to *always* re-pull the Docker image
            },
            "volumes": [ // optional list of volumes
                {
                    "container_path": "/some_path", // optional, where in the container to mount the volume
                    "host_path": "/var/lib/some_path", // required, the path on the host to mount into the container
                    "mode": "RW", // read-write or read-only
                }
            ]
        },
        "uris": [ // optional list of URIs for Mesos to fetch into the task sandbox
            {
                "value": "http://example.com/test.dat", // required, the URI to download
                "executable": false, // optional, whether or not to make the downloaded file executable
                "extract": true, // optional, whether or not to extract the downloaded file if it's a supported archive type
                "cache": true, // optional, whether or not to use a cached copy of the file if available
            }
        ],
        "env": { // optional map of environment variables
            "FOO": "BAR"
        },
        "labels": { // optional map of job labels
            "KEY": "VALUE"
        }
    }
"""


class CookCli(object):
    def __init__(self, args):
        self._args = args
        self._config = configparser.SafeConfigParser({
            'username': getpass.getuser(),
            'password': 'insecure',
            'base_uri': 'http://localhost:12321'
        })
        self._config.read([os.path.expanduser('~/.cookrc')])
        if not self._config.has_section(CONFIG_SECTION):
            self._config.add_section(CONFIG_SECTION)

        base_uri = args['--base_uri']
        if base_uri is None:
            base_uri = self._config.get(CONFIG_SECTION, 'base_uri')

        username = args['--username']
        if username is None:
            username = self._config.get(CONFIG_SECTION, 'username')

        password = args['--password']
        if password is None:
            password = self._config.get(CONFIG_SECTION, 'password')

        self._client = CookClient(base_uri, username, password)

    def execute(self):
        args = self._args
        if args['run']:
            self.run()
        elif args['status']:
            self.status()
        elif args['delete']:
            self.delete()
        elif args['retry']:
            self.retry()
        elif args['list']:
            self.list()
        elif args['logs']:
            self.logs()

    def run(self):
        if self._args['-']: # Read from stdin
            job = Job.json_load(sys.stdin)
        elif self._args['--file'] is not None: # Read from file
                with open(self._args['--file'], 'r') as f:
                    job = Job.json_load(f)
        elif self._args['--json'] is not None:
            job = Job.json_loads(self._args['--json'])
        else:
            raise ValueError("No job description given")

        try:
            print(self._client.launch(job))
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def status(self):
        jobs = self._args['<job-uuid>']
        try:
            statuses = self._client.status(jobs)
            print_jobs(statuses)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def delete(self):
        jobs = self._args['<job-uuid>']
        try:
            self._client.delete(jobs)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def retry(self):
        if len(self._args['<job-uuid>']) != 1:
            print("Only one job can be restarted at a time")
            return
        job = self._args['<job-uuid>']
        retries = int(self._args['<retries>'])
        try:
            res = self._client.retry_job(job, retries)
            print(res)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def list(self):
        user = self._args['<user>']
        states = self._args['<states>']
        limit = self._args['<limit>']
        start_ms = self._args['<start_ms>']
        end_ms = self._args['<end_ms>']
        try:
            jobs = self._client.list_jobs(user, states, start_ms, end_ms, limit)
            print_jobs(jobs)
        except HTTPError as e:
            print("ERROR: {}".format(e.response.text))

    def logs(self):
        job_id = self._args['<job-uuid>']
        if self._args['--stdout']:
            path = 'stdout'
        elif self._args['--stderr']:
            path = 'stderr'
        try:
            fetcher = FileFetcher(self._client.username, self._client.password)
            job = self._client.status(job_id)[0].get()
            for instance in job.get('instances', []):
                print('\nInstance  {}:\n'.format(instance['task_id']))
                print(fetcher.get(instance, path))
        except HTTPError as e:
            print("ERROR: {} {}".format(e.response.status_code, e.response.text))


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
    args = docopt(__doc__, version='Cook CLI {}'.format(__version__))
    CookCli(args).execute()

if __name__ == '__main__':
    main()
