from django.contrib.auth.models import User
from django.contrib import auth as django_auth
from django.contrib.auth import login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

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
            logger.error("[PYAUTH0JWT][DEBUG][validate_jwt] - Invalid JWT Token.")
            payload = None
        except jwt.ExpiredSignatureError as err:
            logger.error(str(err))
            logger.error("[PYAUTH0JWT][DEBUG][validate_jwt] - JWT Expired.")
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
        logger.error("[PYAUTH0JWT][DEBUG][jwt_login] - Could not log user in.")

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
        logger.debug("[PYAUTH0JWT][DEBUG][authenticate] - Attempting to Authenticate User.")

        try:
            user = User.objects.get(username=token_dictionary["email"])
        except User.DoesNotExist:
            logger.debug("[PYAUTH0JWT][DEBUG][authenticate] - User not found, creating.")

            user = User(username=token_dictionary["email"], email=token_dictionary["email"])
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


