# -*- coding: utf-8 -*-
"""
    datastore_client

    :license: see LICENSE for details.
"""
import os
import json

from google.cloud import datastore
from google.oauth2.service_account import Credentials
from werkzeug.local import LocalProxy


class DataStoreConnection(object):
    _instance = None
    client = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def get_client(self):
        if self.client is None or self.client._credentials.expired:
            self.client = self.new_datastore_client()
        return self.client

    @classmethod
    def new_datastore_client(cls):
        """
        Return an authenticated instance of google datastore
        """
        if 'GCP_SERVICE_ACCOUNT_INFO' in os.environ:
            credentials = Credentials.from_service_account_info(
                json.loads(os.environ['GCP_SERVICE_ACCOUNT_INFO'])
            )
        elif 'GCP_SERVICE_ACCOUNT_FILE' in os.environ:
            credentials = Credentials.from_service_account_file(
                json.loads(os.environ['GCP_SERVICE_ACCOUNT_FILE'])
            )
        else:
            credentials = None

        return datastore.Client(
            credentials=credentials,
            project=os.environ.get('GCP_PROJECT'),
            namespace=os.environ.get('GCP_DATASTORE_NAMESPACE')
        )


datastore_client = LocalProxy(DataStoreConnection().get_client)
