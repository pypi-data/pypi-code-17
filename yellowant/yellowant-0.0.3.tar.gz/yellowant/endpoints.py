# -*- coding: utf-8 -*-

"""
yellowant.endpoints
~~~~~~~~~~~~~~~~~~~~~
"""

import os
import warnings
from io import BytesIO
from time import sleep
#try:
    #from StringIO import StringIO
#except ImportError:
    #from io import StringIO

from .advisory import YellowAntDeprecationWarning


class Endpoints(object):

    def get_user_profile(self, **params):
        """Returns the profile for the authenticating user.

        Docs:
        https://dev.yellowant.com/docs/api/1.1/get/statuses/mentions_timeline

        """
        return self.get('user/profile/', params=params)

    def create_user_integration(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile background image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image

        """
        return self.post('user/integration/', params=params)

    def delete_user_integration(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile background image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image

        """
        return self.delete('user/integration/%s' % params.get('id'), params=params)

    def update_user_integration(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile background image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image

        """
        return self.patch('user/integration/%s' % params.get('id'), params=params)


    def add_message(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile background image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image

        """
        return self.post('user/message/', params=params)


    def get_application_messages(self, **params):
        """Returns a list of logs by the application for the current user

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline

        """
        return self.patch('user/application/%s/messages' % params.get('id'), params=params)


    def get_application_message(self, **params):
        """Returns a list of logs by the application for the current user

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline

        """
        return self.patch('user/application/%s/messages/%s' % (params.get('id'), params.get('message')), params=params)


    def get_application_logs(self, **params):
        """Returns a list of logs by the application for the current user

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline

        """
        return self.get('user/logs', params=params)

    def get_application_log(self, **params):
        """Returns a single Tweet, specified by the id parameter
        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/show/%3Aid
        """
        return self.get('user/log/%s' % params.get('id'), params=params)


    def get_application_crons(self, **params):
        """Returns a list of cron jobs

        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline

        """
        return self.get('user/crons', params=params)

    def get_application_cron(self, **params):
        """Returns a single Tweet, specified by the id parameter
        Docs: https://dev.twitter.com/docs/api/1.1/get/statuses/show/%3Aid
        """
        return self.get('user/cron/%s' % params.get('id'), params=params)

    def add_application_log(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile background image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image

        """
        return self.post('user/add_application_log', params=params)



    def add_application_cron(self, **params):  # pragma: no cover
        """Updates the authenticating user's profile background image.

        Docs:
        https://dev.twitter.com/docs/api/1.1/post/account/update_profile_background_image

        """
        return self.post('user/add_application_cron', params=params)

    # OAuth
    def invalidate_token(self, **params):  # pragma: no cover
        """Allows a registered application to revoke an issued OAuth 2 Bearer
        Token by presenting its client credentials.

        Docs: https://dev.twitter.com/docs/api/1.1/post/oauth2/invalidate_token

        """
        return self.post('oauth2/invalidate_token', params=params)

    # Help
    def get_twitter_configuration(self, **params):
        """Returns the current configuration used by Twitter

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/configuration

        """
        return self.get('help/configuration', params=params)

    def get_supported_languages(self, **params):
        """Returns the list of languages supported by Twitter along with
        their ISO 639-1 code.

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/languages

        """
        return self.get('help/languages', params=params)

    def get_privacy_policy(self, **params):
        """Returns Twitter's Privacy Policy

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/privacy

        """
        return self.get('help/privacy', params=params)

    def get_tos(self, **params):
        """Return the Twitter Terms of Service

        Docs: https://dev.twitter.com/docs/api/1.1/get/help/tos

        """
        return self.get('help/tos', params=params)

    def get_application_rate_limit_status(self, **params):
        """Returns the current rate limits for methods belonging to the
        specified resource families.

        Docs:
        https://dev.twitter.com/docs/api/1.1/get/application/rate_limit_status

        """
        return self.get('application/rate_limit_status', params=params)


# from https://dev.twitter.com/docs/error-codes-responses
YELLOWANT_HTTP_STATUS_CODE = {
    200: ('OK', 'Success!'),
    304: ('Not Modified', 'There was no new data to return.'),
    400: ('Bad Request', 'The request was invalid. An accompanying \
          error message will explain why. This is the status code \
          will be returned during rate limiting.'),
    401: ('Unauthorized', 'Authentication credentials were missing \
          or incorrect.'),
    403: ('Forbidden', 'The request is understood, but it has been \
          refused. An accompanying error message will explain why. \
          This code is used when requests are being denied due to \
          update limits.'),
    404: ('Not Found', 'The URI requested is invalid or the resource \
          requested, such as a user, does not exists.'),
    406: ('Not Acceptable', 'Returned by the Search API when an \
          invalid format is specified in the request.'),
    410: ('Gone', 'This resource is gone. Used to indicate that an \
          API endpoint has been turned off.'),
    422: ('Unprocessable Entity', 'Returned when an image uploaded to \
          POST account/update_profile_banner is unable to be processed.'),
    429: ('Too Many Requests', 'Returned in API v1.1 when a request cannot \
          be served due to the application\'s rate limit having been \
          exhausted for the resource.'),
    500: ('Internal Server Error', 'Something is broken. Please post to the \
          group so the Twitter team can investigate.'),
    502: ('Bad Gateway', 'Twitter is down or being upgraded.'),
    503: ('Service Unavailable', 'The Twitter servers are up, but overloaded \
          with requests. Try again later.'),
    504: ('Gateway Timeout', 'The Twitter servers are up, but the request \
          couldn\'t be serviced due to some failure within our stack. Try \
          again later.'),
}
