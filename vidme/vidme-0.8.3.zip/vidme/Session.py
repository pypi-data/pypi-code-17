
# import readline
import api

class Session:

	def __init__(self, settings, no_output = False):
		self.no_output = no_output

		if 'username' in settings and settings['username']:
			self.username = settings['username']
		else:
			self.username = None

		if 'password' in settings and settings['password']:
			self.password = settings['password']
		else:
			self.password = None

		if 'token' in settings and settings['token']:
			self.token = settings['token']
		else:
			self.new_token()

	def get_token(self):
		return self.token['token']

	def new_token(self):
		if not self.no_output:
			print '[-] Your token is invalid or has expired!'

		if not self.username:
			username = raw_input("Please enter your username: ")
		else:
			username = self.username

		if not self.password:
			password = raw_input("Please enter your password: ")
		else:
			password = self.password

		request = api.request('/auth/create', data=dict(
			username=username,
			password=password,
			Authorization="Basic"
		))

		if request:
			self.token = request['auth']
			return True
		else:
			return False
