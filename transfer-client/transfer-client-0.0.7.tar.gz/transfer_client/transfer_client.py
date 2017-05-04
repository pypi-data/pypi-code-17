import json
import requests
import requests_toolbelt
import sys
import urllib3


class TransferClient(object):
    def __init__(self, server_name, verify=True):
        """Initialise the class.

        :arg str server_name: Name or IP of the transfer server.
        :arg bool verify: SSL server certificate verification.
        """
        self.server_name = server_name
        self._verify = verify

        if not self._verify:
            try:
                requests.packages.urllib3.disable_warnings()
            except AttributeError:
                try:
                    urllib3.disable_warnings()
                except AttributeError:
                    sys.stderr = open('/dev/null')

    def _request(self, method, endpoint, headers=None, data=None, json=None):
        """Handle a request.

        :arg str method: Method for the request.
        :arg str endpoint: API endpoint.
        :arg dict headers: Dictionary of HTTP Headers to send with the request.
        :arg dict data: Dictionary of file like objects for multipart encoding
            upload.
        :arg dict json: JSON data to send in the body of the request.

        :returns dict: JSON encoded content of the response.
        """
        try:
            response = requests.request(
                method, 'https://{}/{}'.format(self.server_name, endpoint),
                headers=headers, data=data, json=json, verify=self._verify)
        except requests.exceptions.SSLError:
            raise OSError('SSL error, no server certificate installed?')
        if not response.ok:
            raise ValueError(response.json()['error'])
        return response.json()

    def users(self, user_id):
        """Gives a JSON object of a user together with its transfers.

        :arg str user_id: User ID.

        :returns dict: A JSON object of a user together with its transfers.
        """
        return self._request('get', 'users', {'User-Id': user_id})

    def schema(self, user_id):
        """Gives the JSON schema for a user.

        :arg str user_id: User ID.

        :returns dict: JSON schema.
        """
        return self._request('get', 'users/schema', {'User-Id': user_id})

    def transfers(self, user_id, metadata, name):
        """Initiates a new transfer.

        :arg str user_id: User ID.
        :arg dict metadata: Metadata.
        :arg str name: Name of the metadata file.

        :returns dict: Transfer JSON object.
        """
        multipart = requests_toolbelt.MultipartEncoder(
            fields={'metadata': (name, json.dumps(metadata))})
        return self._request(
            'post', 'transfers',
            {'User-Id': user_id, 'Content-Type': multipart.content_type},
            multipart)

    def status(self, user_id, transfer_id):
        """Gives a JSON object of a transfer.

        :arg str user_id: User ID.
        :arg str transfer_id: Transfer ID.

        :returns dict: Transfer JSON object.
        """
        return self._request(
            'get', 'transfers/{}'.format(transfer_id), {'User-Id': user_id})

    def update(self, user_id, transfer_id, status):
        """Updates a transfer.

        :arg str user_id: User ID.
        :arg str transfer_id: Transfer ID.
        :arg str status: New transfer status.

        :returns dict: Transfer JSON object.
        """
        return self._request(
            'put', 'transfers/{}'.format(transfer_id), {'User-Id': user_id},
            json={'status': status})

    def uploads(self, user_id, transfer_id, file_handle):
        """Uploads a file to a transfer.

        :arg str user_id: User ID.
        :arg str transfer_id: Transfer ID.
        :arg handle file_handle: Open readable file handle.

        :returns dict: Transfer JSON object.
        """
        multipart = requests_toolbelt.MultipartEncoder(
            fields={'upload': (file_handle.name, file_handle)})
        return self._request(
            'post', 'transfers/{}/uploads'.format(transfer_id),
            {'User-Id': user_id, 'Content-Type': multipart.content_type},
            multipart)

    def completed(self, client_id):
        """Gives a JSON object of all transfers for this client, i.e., a list
        of transfer ids.

        :arg str client_id: Client ID.

        :returns dict: JSON object of all transfers.
        """
        return self._request('get', 'completed', {'Client-Id': client_id})
