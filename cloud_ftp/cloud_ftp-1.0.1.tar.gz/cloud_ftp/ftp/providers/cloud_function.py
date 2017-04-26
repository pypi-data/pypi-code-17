# Copyright 2017 Real Kinetic, LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

"""
Implements a simple provider that hits up an external service to move a file
using Google Cloud Functions.  Google Cloud Functions are ridiculously simple
and get around app engine's FTP limitations.  The cloud function moves the
file from an FTP server to GCS.
"""
import json

from google.appengine.api import app_identity
from google.appengine.api import urlfetch

from cloud_ftp import error
from cloud_ftp.ftp import FTPProvider

# defines the time, in seconds, we wait for a cloud ftp function response
DEFAULT_DEADLINE = 30


class CloudFunctionProvider(FTPProvider):
    """Moves FTP files from FTP servers to GCS using cloud functions.  The
    function must be up and running and is hit simply by a normal HTTP
    call, providing information re host, file name, etc.
    """
    def __init__(self, url, bucket_name=None):
        """Initializes this provider with the provided bucket name.  If no
        bucket name is provided, the application's default GCS bucket name
        from app_identity is used.  The URL is required as, as yet, there is
        no convenient way of standardizing on this.  An example would be:

        `https://us-central1-test-project.cloudfunctions.net/importFTP`

        :param url: URL of the cloud function
        :type url: str
        :param bucket_name: name of the bucket to use, if something other than
            default is desired
        :type bucket_name: str or None
        """
        self._url = url
        self._bucket_name = bucket_name \
            or app_identity.get_default_gcs_bucket_name()

    def move_file(self, ctx):
        """Visits the cloud function and has it move the FTP file to GCS.

        :param ctx: information about the request
        :type ctx: src.ftp.Context
        :return: the name of the moved file
        :rtype: str
        """
        response = urlfetch.fetch(
            self._url,
            payload=self.make_data(ctx),
            headers={"Content-Type": "application/json"},
            method=urlfetch.POST,
            deadline=DEFAULT_DEADLINE,
        )
        # ensure we got the correct response
        return self.verify_response(ctx, response)

    def make_data(self, ctx):
        """Makes the json payload required for the request.  Returned is the
        jsonified data.

        :param ctx: information about the request
        :type ctx: src.ftp.Context
        :return: jsonified data
        :rtype: str
        """
        return json.dumps({
            "bucketName": self._bucket_name,
            "host": ctx.host,
            "user": ctx.username,
            "password": ctx.password,
            "fileName": ctx.file_name,
        })

    def verify_response(self, ctx, response):
        """Verifies the response object.  Raises an exception if the response
        indicates it was warranted.

        :param ctx: information about the request
        :type ctx: src.ftp.Context
        :param response: response object from urlfetch.fetch
        :type response: urlfetch.Response
        :return: file name or raises exception
        :rtype: str
        """
        if response.status_code != 200:
            if response.status_code == 404:
                raise error.FileNotFoundError()

            if response.status_code == 401:
                raise error.UnauthorizedError()

            # TODO: correct this to be specific
            raise ValueError('response: {}'.format(response.status_code))

        return ctx.file_name
