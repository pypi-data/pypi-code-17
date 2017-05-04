import base64

from ppg_common.clients.base import BaseClient


class BlossomClient(BaseClient):
    urls = {
        "all_users": "/v0/users/",
        "user": "/v0/users/{}",
        "login": "/v0/users/actions/login/"
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(BlossomClient, self).__init__(host, port, ssl, session)

    def get_users(self):
        return self.get(BlossomClient.urls['all_users'])

    def get_user(self, uid):
        return self.get(BlossomClient.urls['user'].format(uid))

    def delete_user(self, uid):
        return self.delete(BlossomClient.urls['user'].format(uid))

    def create_user(self, username, email, password):
        body = {
            'username': username,
            'email': email,
            'password': str(base64.b64encode(bytes(password, 'utf-8')))
        }
        return self.post(BlossomClient.urls['all_users'], body=body)

    def edit_user(self, uid, username=None, email=None, password=None):
        body = {}
        if username is not None:
            body.update({'username': username})
        if username is not None:
            body.update({'email': email})
        if username is not None:
            body.update(
                {'password': str(base64.b64encode(bytes(password, 'utf-8')))})
        return self.patch(BlossomClient.urls['user'].format(uid), body=body)

    def login_user(self, email, password):
        body = {
            'email': email,
            'password': base64.b64encode(bytes(password, 'utf-8')).decode(
                "utf-8")
        }
        return self.post(BlossomClient.urls['login'], body=body)
