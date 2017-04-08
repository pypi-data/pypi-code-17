import os
import json
import urllib
import logging
import pkg_resources

from .command import Command
from ..utils import WaitCompletion

logger = logging.getLogger(__name__)


class Deployments(Command):
    def __init__(self, *args, **kwargs):
        super(Deployments, self).__init__(*args, **kwargs)

    def list(self, all=False):
        uri = 'deployments/'
        all = self.api.get(uri=uri)
        return all

    @WaitCompletion(logger=logger)
    def create(self, name, file, wait):
        logger.debug('Going to create deployment: {0}'.format(name))
        uri = 'deployments/'
        query_params = None
        encoded_file_data = urllib.quote(file.read().encode("utf-8"))
        data = {"code": encoded_file_data,
                "requirements": "",
                "name": name}
        task_id = self.api.put(uri, params=query_params, data=data, expected_status_code=200)
        return "Execution id: {0}".format(task_id)

    @WaitCompletion(logger=logger)
    def update(self, name, file, new_name, wait):
        logger.debug('Going to update deployment: {0}'.format(name))
        if not (file or new_name):
            return 'No action requested, add --file or --new-name'

        uri = 'deployments/{0}'.format(name)
        query_params = None
        encoded_file_data = urllib.quote(file.read().encode("utf-8")) if file else None
        data = {"requirements": ""}
        if encoded_file_data:
            data['code'] = encoded_file_data
        if new_name:
            data['name'] = new_name
        response = self.api.patch(uri, params=query_params, data=data, expected_status_code=200)
        return response

    def get(self, name):
        logger.debug('Going to retrieve deployment: {0}'.format(name))
        uri = 'deployments/{0}'.format(name)
        response = self.api.get(uri=uri)
        code = response.get('code')
        response['code'] = urllib.unquote(code)
        return response

    def delete(self, name, force):
        logger.debug('Going to delete deployment: {0}'.format(name))
        uri = 'deployments/{0}'.format(name)
        response = self.api.delete(uri=uri)
        return response

    @WaitCompletion(logger=logger)
    def run(self, name, parameters, wait, interval=1):
        """
        :param name:
        :param parameters: the input for the function.
            can be dict of {key: value}
            can be a list of ["key=value",]
            can be a list of [{key: value, }, ] <-- used for bulk run
        :param wait:
        :param interval:
        :return:
        """
        if isinstance(parameters, list) and len(parameters) > 0 and isinstance(parameters[0], dict):
            return self._bulk_run(name, parameters)
        logger.debug('Goring to run `{0}`'.format(name))
        uri = 'deployments/{0}/rpc/'.format(name)
        if isinstance(parameters, dict):
            data = parameters
        elif isinstance(parameters, list):
            data = {p.split('=')[0]: p.split('=')[1] for p in parameters}
        else:
            data = None
        logger.debug('Goring to run `{0}` with parameter: {1}'.format(name, data))
        task_id = self.api.post(uri=uri,
                                data=data)
        return "Execution id: {0}".format(task_id)

    def _bulk_run(self, name, parameters_list):
        uri = 'deployments/{0}/bulk_rpc/'.format(name)
        task_id = self.api.post(uri=uri,
                                data={'values': json.dumps(parameters_list)})
        return task_id

    def samples(self, hello, fib, ping):
        if not (hello or fib or ping):
            return 'No action requested, need to select some sample..'

        name = ''
        if hello:
            name = 'hello.py'
        elif fib:
            name = 'fib.py'
        elif ping:
            name = 'ping.py'
        if os.path.isfile(name):
            return 'File with name `{0}` already exists.'.format(name)
        logger.debug('Going to create a sample file: `{0}`'.format(name))
        resource_package = __name__
        resource_path = '/'.join(('samples', name))
        sample = pkg_resources.resource_stream(resource_package, resource_path)
        content = sample.read()
        with open(name, 'w') as sample_file:
            sample_file.write(content)
        return "Sample file `{0}` been created.".format(name)
