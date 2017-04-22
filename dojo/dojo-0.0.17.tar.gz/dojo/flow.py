from __future__ import unicode_literals

import luigi
import importlib

from datetime import datetime

from luigi.contrib.spark import PySparkTask

from .configurable import Configurable


class Flow(PySparkTask, Configurable):
    name = luigi.Parameter()
    timestamp = luigi.Parameter(default=None)

    REQUIRED = ['config', 'secrets']

    def __init__(self, *args, **kwargs):
        super(Flow, self).__init__(*args, **kwargs)
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def requires(self):
        for task in self._tasks():
            yield task

    def complete(self):
        return False

    def main(self, sc):
        pass

    def _tasks(self):
        datasets = {}
        for name, config in self.config['datasets'].items():
            frequency = config.get('frequency', 'microsecond')
            task = self._adapter_class(config['adapter'])(
                dataset=name,
                frequency=frequency,
                timestamp=self.timestamp
            )
            task.configure(config=config,
                           secrets=self.secrets.get('datasets', {}).get(name, {}),
                           store=self._store(name),
                           error_handler=self._error_handler(name),
                           log_adapter=self._log_adapter(name))
            datasets[name] = task
        for name, config in self.config['datasets'].items():
            datasets[name].depends_on = [datasets[d] for d in config.get('depends_on', [])]

        tasks_by_dependent = {name: [] for name in datasets.keys()}
        for name, task in datasets.items():
            for dependent in task.depends_on:
                tasks_by_dependent[dependent.dataset].append(name)
        return [datasets[name] for name, tasks in tasks_by_dependent.items() if len(tasks) == 0]

    def _store(self, dataset_name):
        return self._adapter_class(self.config['store']['adapter'])(
            config=self.config['store'],
            secrets=self.secrets.get('store', {}),
            dataset=dataset_name)

    def _error_handler(self, dataset_name):
        if 'errors' not in self.config:
            return None
        return self._adapter_class(self.config['errors']['adapter'])(
            config=self.config['errors'],
            secrets=self.secrets.get('errors', {}),
            dataset=dataset_name)

    def _log_adapter(self, dataset_name):
        if 'logs' not in self.config:
            return None
        return self._adapter_class(self.config['logs']['adapter'])(
            config=self.config['logs'],
            secrets=self.secrets.get('logs', {}),
            dataset=dataset_name)

    def _adapter_class(self, adapter_path):
        adapter_parts = adapter_path.split('.')
        adapter_module = importlib.import_module('.'.join(adapter_parts[:-1]))
        return getattr(adapter_module, adapter_parts[-1])
