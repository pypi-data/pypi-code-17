import requests


class FileFetcher(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def _auth(self):
        return self.username, self.password

    def find_directory(self, task_id, hostname):
        state_url = 'http://{}:5051/state'.format(hostname)
        req = requests.get(state_url, auth=self._auth)
        req.raise_for_status()
        state = req.json()
        for framework in state['completed_frameworks'] + state['frameworks']:
            for executor in framework['completed_executors'] + framework['executors']:
                for task in executor['queued_tasks'] + executor['tasks'] + executor['completed_tasks']:
                    if task['id'] == task_id:
                        return executor['directory']
        return None

    def fetch_file(self, task_id, hostname, path):
        url = 'http://{}:5051/files/download'.format(hostname)
        path = self.find_directory(task_id, hostname) + '/' + path
        req = requests.get(url, {'path': path}, auth=self._auth)
        req.raise_for_status()
        return req.text

    def get(self, instance, path):
        return self.fetch_file(instance['task_id'], instance['hostname'], path)
