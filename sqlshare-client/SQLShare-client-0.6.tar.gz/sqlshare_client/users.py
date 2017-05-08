import json


class Users(object):
    def __init__(self, oauth):
        self.oauth = oauth

    def get_current_user(self):
        data = self.oauth.request("/v3/user/me")
        return self._build_user(data)

    def _build_user(self, data):
        data = json.loads(data)
        return User(data)


class User(object):
    def __init__(self, data={}):
        for key in data:
            setattr(self, key, data[key])

    def __str__(self):
        return "User %s" % self.username
