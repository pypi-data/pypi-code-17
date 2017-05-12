from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password, password_changed, password_validators_help_texts
from django.db.models import Q
from rest_framework.authtoken.models import Token
from ohm2_handlers_light import utils as h_utils
from ohm2_accounts_light import settings
import importlib


def create_user(username, email, password, **kwargs):

	user = User.objects.create_user(username = username,
								    email = email,
								    password = password)
	

	return user

def get_user(**kwargs):
	return h_utils.db_get(User, **kwargs)

def get_or_none_user(**kwargs):
	return h_utils.db_get_or_none(User, **kwargs)

def filter_user(**kwargs):
	return h_utils.db_filter(obj = User, **kwargs)

def get_or_create_authtoken(user):
	token, created = Token.objects.get_or_create(user = user)
	return token

def get_authtoken(user):
	return Token.objects.get(user = user)

def user_exist(**kwargs):
	if filter_user(**kwargs).count() > 0:
		return True
	return False

def change_password(user, password):
	user.set_password(password)
	user.save()
	return user

def user_authenticate(username, password):
	return authenticate(username = username, password = password)

def user_login(request, auth_user):
	return login(request, auth_user)

def user_logout(request):
	return logout(request)

def validate_current_password(password, user = None, password_validators = None):
	try:
		validate_password(password, user, password_validators)
	except ValidationError as e:
		return [reason for reason in e]
	return []

def is_password_secure(password, user = None, password_validators = None):
	errors = validate_current_password(password, user, password_validators)
	if len(errors) == 0:
		return True
	return False

def run_login_pipeline(request, auth_user, **kwargs):
	previous_outputs = {}
	for pipeline in settings.LOGIN_PIPELINE:

		func = pipeline.rsplit(".", 1)[-1]
		
		m = importlib.import_module(pipeline)
		function = getattr(m, func)

		auth_user, output = function(request, auth_user, previous_outputs)

		previous_outputs = h_utils.join_dicts(previous_outputs, output)

	return None

def run_logout_pipeline(request, **kwargs):
	previous_outputs = {}
	for pipeline in settings.LOGOUT_PIPELINE:

		func = pipeline.rsplit(".", 1)[-1]
		
		m = importlib.import_module(pipeline)
		function = getattr(m, func)

		output = function(request, previous_outputs)

		previous_outputs = h_utils.join_dicts(previous_outputs, output)

	return None	