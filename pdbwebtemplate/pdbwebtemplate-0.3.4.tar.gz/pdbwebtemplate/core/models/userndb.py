'''
Created on Nov 28, 2016
@author: everton
'''
import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb
from google.appengine.api import namespace_manager
import os
import time

try:
    from ndb import model
except ImportError:
    from google.appengine.ext.ndb import model


class UserNdb(webapp2_extras.appengine.auth.models.User):
    identifier = ndb.StringProperty()


    @classmethod
    def create_signup_token(cls, user_id):
        """Creates a new SIGNUP token for a given user ID.
        :param user_id:
            User unique ID.
        :returns:
            A string with the SIGNUP token.
        """
        promoname = os.environ['PROMO_NAME']
        namespace_manager.set_namespace(promoname)
        return cls.token_model.create(user_id, 'signup').key.id()

    @classmethod
    def get_valid_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            A tuple ``(User, timestamp)``, with a user object and
            the token timestamp, or ``(None, None)`` if both were not found.
        """
        promoname = os.environ['PROMO_NAME']
        namespace_manager.set_namespace(promoname)

        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = model.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user_model = model.get_multi([token_key, user_key])
        if valid_token:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return valid_token, timestamp

        Exception('InvalidToken')
