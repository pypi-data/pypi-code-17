import requests


class Project:
	domain = 'http://api.datanorth.io/'

	def __init__(self, name):
		self.name = name
		self.full_name = self.domain + self.name + '/'

	@property
	def endpoints(self):
		r = requests.get(self.full_name)
		return r.json()


	def scan(self, key):
		r = requests.get(self.full_name + key)
		return r.json()
