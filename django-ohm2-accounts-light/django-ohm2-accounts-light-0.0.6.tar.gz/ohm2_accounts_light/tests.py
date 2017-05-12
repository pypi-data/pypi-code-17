from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from rest_framework.test import APIClient
from ohm2_handlers_light import utils as h_utils
from ohm2_accounts_light import utils as ohm2_accounts_light_utils
from ohm2_accounts_light import settings

try:
	import simplejson as json
except Exception:
	import json


							 	
class ApiTestCase(TestCase):
	
	test_username = "testusername"
	test_email = "test@email.com"
	test_password = h_utils.random_string(10)
	
		
	def setUp(self):
		
		user = ohm2_accounts_light_utils.create_user(self.test_username, self.test_email, self.test_password)		
		

	def test_signup_success(self):
		SIGNUPS_ENABLED_ORIGINAL = settings.SIGNUPS_ENABLED
		settings.SIGNUPS_ENABLED = True	

		c = APIClient()
		url = reverse("ohm2_accounts_light:api_v1:signup")
		
		data = {
			"username" : h_utils.random_string(10),
			"password" : h_utils.random_string(10),
		}
		response = c.post(url, data, format = 'json')
		self.assertEqual(response.status_code, 200)

		res = response.json()
		error = True if res["error"] else False
		if error:
			print(res["error"])

		self.assertEqual(error, False)	
		settings.SIGNUPS_ENABLED = SIGNUPS_ENABLED_ORIGINAL
		
	
	def test_login_fail(self):
		
		c = APIClient()
		url = reverse("ohm2_accounts_light:api_v1:login")
		
		data = {
			"username" : self.test_username,
			"password" : h_utils.random_string(10),
		}
		response = c.post(url, data, format = 'json')
		self.assertEqual(response.status_code, 200)

		res = response.json()
		error = True if res["error"] else False
		
		self.assertEqual(error, True)	
	

	def test_login_success(self):
		
		c = APIClient()
		url = reverse("ohm2_accounts_light:api_v1:login")
		
		data = {
			"username" : self.test_username,
			"password" : self.test_password,
		}
		response = c.post(url, data, format = 'json')
		self.assertEqual(response.status_code, 200)

		res = response.json()
		error = True if res["error"] else False
		if error:
			print(res["error"])

		self.assertEqual(error, False)

	
	def test_logout_success(self):
		
		c = APIClient()
		c.login(username = self.test_username, password = self.test_password)

		url = reverse("ohm2_accounts_light:api_v1:logout")
		
		data = {
		}

		response = c.post(url, data, format = 'json')
		self.assertEqual(response.status_code, 200)

		res = response.json()
		error = True if res["error"] else False
		if error:
			print(res["error"])

		self.assertEqual(error, False)		


	def test_signup_and_get_token_success(self):
		SIGNUPS_ENABLED_ORIGINAL = settings.SIGNUPS_ENABLED
		settings.SIGNUPS_ENABLED = True	

		c = APIClient()
		url = reverse("ohm2_accounts_light:api_v1:signup_and_get_token")
		
		data = {
			"username" : h_utils.random_string(10),
			"password" : h_utils.random_string(10),
		}
		response = c.post(url, data, format = 'json')
		self.assertEqual(response.status_code, 200)

		res = response.json()
		error = True if res["error"] else False
		if error:
			print(res["error"])

		self.assertEqual(error, False)	
		settings.SIGNUPS_ENABLED = SIGNUPS_ENABLED_ORIGINAL	
	

	def test_login_and_get_token_fail(self):
		
		c = APIClient()
		url = reverse("ohm2_accounts_light:api_v1:login_and_get_token")
		
		data = {
			"username" : self.test_username,
			"password" : h_utils.random_string(10),
		}
		response = c.post(url, data, format = 'json')
		self.assertEqual(response.status_code, 200)

		res = response.json()
		error = True if res["error"] else False
		self.assertEqual(error, True)

	def test_login_and_get_token_success(self):
		
		c = APIClient()
		url = reverse("ohm2_accounts_light:api_v1:login_and_get_token")
		
		data = {
			"username" : self.test_username,
			"password" : self.test_password,
		}
		response = c.post(url, data, format = 'json')
		self.assertEqual(response.status_code, 200)

		res = response.json()
		error = True if res["error"] else False
		if error:
			print(res["error"])

		self.assertEqual(error, False)
		


