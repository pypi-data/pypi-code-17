"""Contain functions to manage script arguments
and RequestApi class to communicate with the distant
AskOmics server"""

import os
from os.path import basename
import json
import requests
# import logging

# logging.getLogger('requests').setLevel(logging.CRITICAL)
# log = loggin.getLoger()

def askomics_auth(parser):
    """manage authentication arguments

    :param parser: the parser
    :type parser: argparse
    """

    parser.add_argument('-k', '--apikey', help='An API key associate with your account', required=True)

def askomics_url(parser):
    """manage askomics arguments

    :param parser: the parser
    :type parser: argparse
    """

    parser.add_argument('-a', '--askomics', help='AskOmics URL', required=True)
    parser.add_argument('-p', '--port', help='AskOmics port')


class RequestApi(object):
    """RequestApi contain method to communicate with
    the AskOmics API"""


    def __init__(self, url, apikey, file_type):

        self.url = url
        self.cookies = None
        self.headers = {'X-Requested-With': 'XMLHttpRequest'}
        self.apikey = apikey
        self.col_types = None
        self.key_columns = [0] # Default value
        self.path = None
        self.type = file_type
        self.public = False
        self.disabled_columns = []

    def set_cookie(self):
        """set the session cookie of user

        :returns: session cookie of user
        :rtype: cookies
        """

        json_dict = {
            'apikey': self.apikey
        }

        url = self.url + '/login_api'

        response = requests.post(url, json=json_dict)

        if response.status_code != 200:
            raise Exception('Unexpected response from AskOmics when login: ' +
                            str(response.status_code) + '\n' + response.text)

        # Check the passwd
        if 'error' in json.loads(response.text):
            if json.loads(response.text)['error']:
                raise Exception('AskOmics error: ' + str(json.loads(response.text)['error']))

        cookies = response.cookies

        self.cookies = cookies

    def upload_file(self):
        """Upload a file into tmp dir of user

        :returns: the response dict
        :rtype: dict
        """

        url = self.url + '/up/file'
        files = {
            basename(self.path): open(self.path, 'rb')
        }

        response = requests.post(url, files=files, cookies=self.cookies, headers=self.headers)

        if response.status_code != 200:
            raise Exception('Unexpected response from AskOmics when uploading a file: ' +
                            str(response.status_code) + '\n' + response.text)

        if 'error' in json.loads(response.text):
            raise Exception('AskOmics error: ' + str(json.loads(response.text)['error']))

        return response.text

    def set_key_columns(self, keycols):
        """Set the key columns

        :param keycols: list of key index
        :type keycols: list
        """
        new_list = []
        for index in keycols:
            new_list.append(int(index))

        self.key_columns = new_list

    def set_filepath(self, path):
        """set the file path"""

        self.path = path

    def force_col_types(self, forced_types):
        """Force the columns types of a csv file

        :param forced_types: list of the forced types
        :type forced_types: list
        """

        self.col_types = forced_types
        self.col_types[0] = 'entity_start'

    def set_visibility(self, visibility):
        """Set the visibility of the dataset

        True for public and False for private

        :param visibility: The visibility
        :type visibility: boolean
        """

        self.public = visibility

    def set_disabled_columns(self, disabled_columns):
        """Set the diabled columns

        :param disabled_columns: List if index to disable
        :type disabled_columns: list
        """

        new_list = []
        for index in disabled_columns:
            new_list.append(int(index))

        self.disabled_columns = new_list

    def guess_col_types(self):
        """Guess the colomns type of a csv file"""

        url = self.url + '/guess_csv_header_type'

        json_dict = {
            'filename': basename(self.path)
        }

        response = requests.post(url, cookies=self.cookies, headers=self.headers, json=json_dict)

        if response.status_code != 200:
            raise Exception('Unexpected response from AskOmics when guessing col types: ' +
                            str(response.status_code) + '\n' + response.text)

        if 'error' in json.loads(response.text):
            raise Exception('AskOmics error: ' + str(json.loads(response.text)['error']))


        self.col_types = json.loads(response.text)['types']
        self.col_types[0] = 'entity_start'


    def integrate_data(self):
        """Integrate the csv file into the triplestore

        :returns: response text
        :rtype: string
        """


        url = self.url + '/load_data_into_graph'


        json_dict = {
            'file_name': basename(self.path),
            'col_types': self.col_types,
            'disabled_columns': self.disabled_columns,
            'key_columns': self.key_columns,
            'public': self.public,
            'forced_type': self.type
        }

        response = requests.post(url, cookies=self.cookies, headers=self.headers, json=json_dict)

        if response.status_code != 200:
            raise Exception('Unexpected response from AskOmics when integrate csv: ' +
                            str(response.status_code) + '\n' + response.text)

        if 'error' in json.loads(response.text):
            raise Exception('AskOmics error: ' + str(json.loads(response.text)['error']))

        return response.text

    def integrate_gff(self, taxon, entities):
        """Integrate a gff into the triplestore

        :param taxon: taxon
        :type taxon: string
        :param entities: list of entities to integrate
        :type entities: list
        :returns: response text
        :rtype: string
        """

        url = self.url + '/load_gff_into_graph'

        json_dict = {
            'file_name': basename(self.path),
            'taxon': taxon,
            'entities': entities,
            'public': self.public,
            'forced_type': self.type
        }

        response = requests.post(url, cookies=self.cookies, headers=self.headers, json=json_dict)

        if response.status_code != 200:
            raise Exception('Unexpected response from AskOmics when integrate gff: ' +
                            str(response.status_code) + '\n' + response.text)

        if 'error' in json.loads(response.text):
            raise Exception('AskOmics error: ' + str(json.loads(response.text)['error']))

        return response.text

    def integrate_ttl(self):
        """Integrate a ttl into the triplestore

        :returns: response text
        :rtype: string
        """

        url = self.url + '/load_ttl_into_graph'

        json_dict = {
            'file_name': basename(self.path),
            'public': self.public,
            'forced_type': self.type
        }

        response = requests.post(url, cookies=self.cookies, headers=self.headers, json=json_dict)

        if response.status_code != 200:
            raise Exception('Unexpected response from AskOmics when integrate ttl: ' +
                            str(response.status_code) + '\n' + response.text)

        if 'error' in json.loads(response.text):
            raise Exception('AskOmics error: ' + str(json.loads(response.text)['error']))

        return response.text
