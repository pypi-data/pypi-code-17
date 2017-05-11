from ohm2_accounts_light.decorators import ohm2_accounts_light_safe_request
from ohm2_accounts_light import utils as ohm2_accounts_light_utils
from ohm2_accounts_light import settings
from . import errors




@ohm2_accounts_light_safe_request
def signup(request, params):
	p = h_utils.cleaned(params,
						(
							("string", "username", 1),
							("string", "password", 1),
							("string", "email", 0),
						))


	
	if request.user.is_authenticated():
		return {"error": errors.USER_ALREADY_LOGGED_IN}
	
	elif ohm2_accounts_light_utils.user_exist(username = p["username"]):
		return {"error" : errors.USER_ALREADY_EXIST}

	elif settings.CHECK_PASSWORD_SECURE and not ohm2_accounts_light_utils.is_password_secure(p["password"]):
		return {"error" : errors.THE_PASSWORD_IS_NOT_SECURE}

	elif len(p["email"]) > 0 and not h_utils.is_email_valid(p["email"]):
		return {"error" : errors.INVALID_EMAIL}

	elif not settings.SIGNUPS_ENABLED:
		return {"error" : errors.SIGNUPS_DISABLED}

	else:
		pass


	username, password, email = p["username"], p["password"], p["email"]

	if len(email) == 0 and h_utils.is_email_valid(username):
		email = username

	
	user = ohm2_accounts_light_utils.create_user(username, email, password)

	ret = {
		"error" : None,
		"ret" : True,
	}
	return ret



@ohm2_accounts_light_safe_request
def login(request, params):
	p = h_utils.cleaned(params,
						(
							("string", "username", 1),
							("string", "password", 1),
							("string", "email", 0),
						))


	
	

	ret = {
		"error" : None,
		"ret" : True,
	}
	return ret
