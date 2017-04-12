from django.contrib.auth.models import User
from django.contrib import auth as django_auth
from django.contrib.auth import login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

import jwt
import base64
import logging
logger = logging.getLogger(__name__)


def user_auth_and_jwt(function):
    def wrap(request, *args, **kwargs):

        # Validates the JWT and returns its payload if valid.
        jwt_payload = validate_jwt(request)

        # User is both logged into this app and via JWT.
        if request.user.is_authenticated() and jwt_payload is not None:
            return function(request, *args, **kwargs)
        # User has a JWT session open but not a Django session. Start a Django session and continue the request.
        elif not request.user.is_authenticated() and jwt_payload is not None:
            if jwt_login(request, jwt_payload):
                return function(request, *args, **kwargs)
            else:
                return logout_redirect(request)
        # User doesn't pass muster, throw them to the login app.
        else:
            return logout_redirect(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def validate_jwt(request):
    """
    Determines if the JWT is valid based on expiration and signature evaluation.
    :param request: 
    :return: None if JWT is invalid or missing.
    """
    # Extract JWT token into a string.
    jwt_string = request.COOKIES.get("DBMI_JWT", None)

    # Check that we actually have a token.
    if jwt_string is not None:

        # Attempt to validate the JWT (Checks both expiry and signature)
        try:
            payload = jwt.decode(jwt_string,
                                 base64.b64decode(settings.AUTH0_SECRET, '-_'),
                                 algorithms=['HS256'],
                                 leeway=120,
                                 audience=settings.AUTH0_CLIENT_ID)

        except jwt.InvalidTokenError as err:
            logger.error(str(err))
            logger.error("Invalid JWT Token.")
            payload = None
        except jwt.ExpiredSignatureError as err:
            logger.error(str(err))
            logger.error("JWT Expired.")
            payload = None
    else:
        payload = None

    return payload


def jwt_login(request, jwt_payload):
    """
    The user has a valid JWT but needs to log into this app. Do so here and return the status.
    :param request:
    :param jwt_payload: String form of the JWT.
    :return:
    """

    logger.debug("[PYAUTH0JWT][DEBUG][jwt_login] - Logging user in via JWT. Is Authenticated? " + str(request.user.is_authenticated()))

    request.session['profile'] = jwt_payload

    user = django_auth.authenticate(**jwt_payload)

    if user:
        login(request, user)
    else:
        logger.error("Could not log user in.")

    return request.user.is_authenticated()


def logout_redirect(request):
    """
    This will log a user out and redirect them to log in again via the AuthN server.
    :param request: 
    :return: The response object that takes the user to the login page. 'next' parameter set to bring them back to their intended page.
    """
    logout(request)
    response = redirect(settings.AUTHENTICATION_LOGIN_URL + "?next=" + request.build_absolute_uri())
    response.delete_cookie('DBMI_JWT', domain=settings.COOKIE_DOMAIN)

    return response


class Auth0Authentication(object):

    def authenticate(self, **token_dictionary):
        logger.debug("Attempting to Authenticate User - " + token_dictionary["email"])

        try:
            user = User.objects.get(username=token_dictionary["email"])
        except User.DoesNotExist:
            logger.debug("User not found, creating.")

            user = User(username=token_dictionary["email"], email=token_dictionary["email"])
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class Auth0JSONWebTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            print("User not found, creating.")

            user = User(username=username, email=username)
            user.save()

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user

