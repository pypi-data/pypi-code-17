'''
Created on Nov 28, 2016

@author: everton
'''
import webapp2_extras.appengine.auth.models
import datetime
from datetime import datetime, timedelta
try:
    from ndb import model
except ImportError:
    from google.appengine.ext.ndb import model

from google.appengine.api import namespace_manager
import os
from pdbwebtemplate.core.configfile import ConfigFile
import logging


class UserToken(webapp2_extras.appengine.auth.models.UserToken):

    def __init__(self, *args, **kwds):
        '''
        It's loading name space during init
        '''
        promoname = os.environ['PROMO_NAME']
        namespace_manager.set_namespace(promoname)
        super(UserToken, self).__init__(*args, **kwds)

    @classmethod
    def get(cls, user=None, subject=None, token=None):
        """Fetches a user token.

        :param user:
            User unique ID.
        :param subject:
            The subject of the key. Examples:

            - 'auth'
            - 'signup'
        :param token:
            The existing token needing verified.
        :returns:
            A :class:`UserToken` or None if the token does not exist.
        """
        if user and subject and token:
            return cls.get_key(user, subject, token).get()

        assert subject and token, \
            'subject and token must be provided to UserToken.get().'
        return cls.query(cls.subject == subject, cls.token == token).get()

    @classmethod
    def validate_token(cls, token_string):
        values = token_string.split('.')
        if len(values) != 3:
            raise Exception('InvalidToken')
        user_id = values[0]
        subject = values[1]
        token = values[2]

        token_instance = cls.get(user_id, subject, token)
        if not token_instance:
            raise Exception("TOKEN_UNAUTHORIZED")
        else:
            time_creation = token_instance.created
            time_now = datetime.now()
            settings = ConfigFile()
            expiration_time = int(settings.get_config_variable('token', 'EXPIRATION_TIME', True))
            logging.info('TIME NOW: '+str(time_now))
            logging.info('TIME CREATION: ' + str(time_creation))
            logging.info('TIME DIFFERENCE: ' + str(time_now - time_creation))
            if (time_now - time_creation) > timedelta(minutes=expiration_time):
                raise Exception("TOKEN_EXPIRED")
            return token_instance

