from __future__ import absolute_import, print_function, unicode_literals

import os
import argparse
import logging
import yaml
import json
import importlib
import fnmatch

from datetime import datetime



class Entrypoint(object):

    def run(self):
        logging.getLogger().setLevel(logging.INFO)

        parser = argparse.ArgumentParser()
        parser.add_argument('name', help='reference to the job that should be run from the config')
        parser.add_argument('--runner', dest='runner', default=None, help='Specify a runner for the job.')
        parser.add_argument('--config', dest='config', default='config/config.yml', help='Configuration file.')
        parser.add_argument('--secrets', dest='secrets', default='config/secrets.json', help='Secrets file.')
        args = parser.parse_args()

        config = self._read_yaml(args.config) or {}
        if 'jobs' not in config:
            config['jobs'] = {}
        jobs_config_dir = os.path.join(os.path.dirname(args.config), 'jobs')
        for config_file in self._list_files_r(jobs_config_dir, 'yml'):
            jobs_config = self._read_yaml(config_file)
            config['jobs'].update(jobs_config['jobs'])
        secrets = self._read_json(args.secrets)
        job = self._build_job(args.name, config, secrets)

        runner_name = 'direct' if args.runner is None else args.runner
        if '.' in runner_name:
            runner_class = self._get_module_class(runner_name)
        else:
            if runner_name not in job.RUNNERS:
                raise ValueError('specified runner "%s" is not supported by job type %s, only %s' % (runner_name, job.__class__.__name__, job.RUNNERS.keys()))
            runner_class = job.RUNNERS[runner_name]

        runner_class().run(job, config)

    def _build_job(self, job_name, config, secrets):
        job_config = config.get('jobs', {}).get(job_name, {})
        job_config.update({
            'name': job_name,
            'timestamp': datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        })
        job_class = self._get_module_class(config['jobs'][job_name]['adapter'])
        job_secrets = secrets.get(job_name, {})
        job_config['store'] = config['store']
        if 'store' in job_config:
            if 'store' not in job_secrets:
                job_secrets['store'] = {}
            job_secrets['store']['connection'] = secrets['connections'].get(job_config['store']['connection'])
        return job_class(job_config, job_secrets)

    def _read_json(self, path):
        with open(path, 'r') as f:
            return json.loads(f.read())

    def _read_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.load(f)

    def _get_module_class(self, module_class_path):
        module_and_class_parts = module_class_path.split('.')
        module = importlib.import_module('.'.join(module_and_class_parts[:-1]))
        return getattr(module, module_and_class_parts[-1])

    def _list_files_r(self, path, extension):
        matches = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.%s' % (extension, )):
                matches.append(os.path.join(root, filename))
        return matches


if __name__ == '__main__':
    Entrypoint().run()
