from __future__ import absolute_import, division, print_function, unicode_literals

import boto3
from configparser import ConfigParser, NoSectionError
from os.path import expanduser, join
import requests
from warrant.aws_srp import AWSSRP

from amaascore.config import COGNITO_REGION, COGNITO_CLIENT_ID, COGNITO_POOL
from amaascore.exceptions import AMaaSException


class Interface(object):
    """
    Currently this class doesn't do anything - but I anticipate it will be needed in the future.
    """

    def __init__(self, endpoint, tokens=None, use_auth=True, config_filename=None):
        # Add authentication routine here
        self.config_filename = config_filename
        self.auth_token = self.read_token() if use_auth is True else ''
        self.endpoint = endpoint
        self.json_header = {'Content-Type': 'application/json'}
        self.session = requests.Session()
        self.tokens = tokens or {}
        auth_token = self.auth_token or self.tokens.get('AccessToken')
        self.session.headers.update({'Authorization': auth_token})

    @staticmethod
    def generate_config_filename():
        home = expanduser("~")
        return join(home, '.amaas.cfg')

    def read_token(self):
        if self.config_filename is None:
            self.config_filename = self.generate_config_filename()
        parser = ConfigParser()
        parser.read(self.config_filename)
        try:
            token = parser.get(section='auth', option='token')
        except NoSectionError:
            raise AMaaSException('Invalid AMaaS config file')
        return token

    def login(self, username, password):
        client = boto3.client('cognito-idp', COGNITO_REGION)
        aws = AWSSRP(username=username, password=password, pool_id=COGNITO_POOL,
                     client_id=COGNITO_CLIENT_ID, client=client)
        self.tokens = aws.authenticate_user()
        return self.tokens
