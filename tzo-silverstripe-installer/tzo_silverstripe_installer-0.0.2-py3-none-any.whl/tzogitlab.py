import requests


class TZOGitLabException(Exception):
    """
    Expection for GitLab
    """
    pass


class TZOGitLab:
    api_url = 'http://git.timezoneone.com/api/v4'
    token = None
    group_name = 'timezoneone'
    group = None

    def __init__(self, token):
        self.token = token
        try:
            response = requests.get(
                self.api_url + '/groups?search=' + self.group_name,
                headers={'PRIVATE-TOKEN': self.token}
            )
        except requests.RequestException:
            raise
        if response.status_code != 200:
            raise TZOGitLabException('Error when trying to connect to GitLab.')
        result = response.json()
        if not isinstance(result, list) or len(result) == 0:
            raise TZOGitLabException('Cannot find TimeZoneOne group in GitLab.')
        self.group = result[0]

    def create_repo(self, name):
        response = requests.post(
            self.api_url + '/projects?name={name}&namespace_id={group_id}'.format(name=name, group_id=self.group['id']),
            headers={'PRIVATE-TOKEN': self.token}
        )
        if response.status_code != 201:
            raise TZOGitLabException(response.json()['message']['name'])
        return response.json()

