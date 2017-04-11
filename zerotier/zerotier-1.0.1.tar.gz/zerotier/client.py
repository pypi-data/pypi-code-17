import requests

from .network_service import  NetworkService 
from .self_service import  SelfService 
from .status_service import  StatusService 
from .user_service import  UserService 


class Client:
    def __init__(self, base_uri = "https://my.zerotier.com/api"):
        self.base_url = base_uri
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
        self.network = NetworkService(self)
        self.self = SelfService(self)
        self.status = StatusService(self)
        self.user = UserService(self)

    def is_goraml_class(self, data):
        # check if a data is go-raml generated class
        # we currently only check the existence
        # of as_json method
        op = getattr(data, "as_json", None)
        if callable(op):
            return True
        return False

    def set_auth_header(self, val):
        ''' set authorization header value'''
        self.session.headers.update({"Authorization":val})

    def get(self, uri, headers, params):
        res = self.session.get(uri, headers=headers, params=params)
        res.raise_for_status()
        return res

    def post(self, uri, data, headers, params):
        if self.is_goraml_class(data):
            res = self.session.post(uri, data=data.as_json(), headers=headers, params=params)
        elif type(data) is str:
            res = self.session.post(uri, data=data, headers=headers, params=params)
        else:
            res = self.session.post(uri, json=data, headers=headers, params=params)
        res.raise_for_status()
        return res

    def put(self, uri, data, headers, params):
        if self.is_goraml_class(data):
            res = self.session.put(uri, data=data.as_json(), headers=headers, params=params)
        elif type(data) is str:
            res = self.session.put(uri, data=data, headers=headers, params=params)
        else:
            res = self.session.put(uri, json=data, headers=headers, params=params)
        res.raise_for_status()
        return res

    def patch(self, uri, data, headers, params):
        if self.is_goraml_class(data):
            res = self.session.patch(uri, data=data.as_json(), headers=headers, params=params)
        elif type(data) is str:
            res = self.session.patch(uri, data=data, headers=headers, params=params)
        else:
            res = self.session.patch(uri, json=data, headers=headers, params=params)
        res.raise_for_status()
        return res