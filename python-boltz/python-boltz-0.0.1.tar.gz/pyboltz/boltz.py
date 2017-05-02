import requests
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint


class Boltz(object):
	
	URL_LOGIN = "https://www.bolt.id/my-bolt"
	URL_SUBMIT = "https://www.bolt.id/my-bolt.login"
	URL_DASHBOARD = "https://www.bolt.id/my-bolt"
	URL_PROFILE = "https://www.bolt.id/my-bolt-edit-profile"
	
	def __init__(self, nomor, password):
		self.__nomor = nomor
		self.__password = password
		self.__token = ""
		self.__user = ""
		self.__pulsa = ""
		self.__quota = ""
		self.__profile = {}
		self.__datamain = {}
		
		# =============================================
		# Inisialisasi sesi awal
		# resource: http://stackoverflow.com/a/16994114
		# =============================================
		self.__session = requests.session()
	
	def data_post(self):
		return {
			"nomor": self.__nomor,
			"password": self.__password,
			"_token": self.__token,
		}
		
	def get_datamain(self, to_json=False):
		self.__datamain = {
			"nomor": self.__nomor,
			"password": self.__password,
			"user": self.__user,
			"token_log": self.__token,
			"pulsa": self.__pulsa,
			"quota": self.__quota,
		}
		
		result = self.__datamain
		
		if to_json:
			result = json.dumps(self.__datamain)
			
		return result
		
	
	def authenticate(self):
		#try:
		# ========================
		# get object document html
		# ========================
		r = self.__session.get(Boltz.URL_LOGIN)
		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'html.parser')
	
		# ====================================================
		# mengambil token dan url login submit dari situs bolt
		# resource: http://stackoverflow.com/a/25284165 
		# ====================================================
		self.__token = soup.find('input', {'name': '_token', 'type': 'hidden'}).get('value')
		Boltz.URL_SUBMIT = soup.find('form', {'id': 'selfcarelogin'})['action']
	
		# =============================================
		# Melakukan login ke situs bolt.
		# resource: http://stackoverflow.com/a/16994114
		# =============================================
		login_data = self.data_post()
		self.__session.post(Boltz.URL_SUBMIT, data=login_data)
		r = self.__session.get(Boltz.URL_LOGIN)
		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'html.parser')
	
		# ========
		# Set user
		# ========
		self.__set_user(soup)
	
		# ===============
		# Set pulsa utama
		# ===============
		self.__set_pulsa_utama(soup)
	
		# =========
		# Set quota
		# =========
		self.__set_quota_utama(soup)
	
		if self.__check_auth():
			return True
	
		return False
		#except:
			#return False
	
	def __check_auth(self):
		auth = True
		for k,v in self.data_post().items():
			if not v:
				auth = False
		
		return auth
		
	def __set_user(self, soup):
		self.__user = soup.find('a', {'class': 'userName'}).text.replace("Hello, ", "")
		
	def __set_pulsa_utama(self, soup):
		tag_div_userdatahome = soup.find('div', {'class': 'userdataHome'})
		# index 1: adalah data extract untuk bagian SALDO PULSA (Rp). 
		tag_li_saldopulsa = tag_div_userdatahome.ul.find_all('li')[0]
		tag_div_datacontent = tag_li_saldopulsa.find('div', {'class': 'dataContent'})
		sample = tag_div_datacontent.find('table').find_all("tr")
		data = {}
		for i in sample:
			# index 1: adalah data extract untuk ukuran SALDO PULSA (Rp) dalam harga. 
			data[i.th.text.replace(' > ', '').replace(' ', '_').lower()] = i.find_all('td')[1].text
		
		self.__pulsa = data
		
	def __set_quota_utama(self, soup):
		tag_div_userdatahome = soup.find('div', {'class': 'userdataHome'})
		# index 1: adalah data extract untuk bagian SALDO KUOTA (GB). 
		tag_li_saldopulsa = tag_div_userdatahome.ul.find_all('li')[1]
		tag_div_datacontent = tag_li_saldopulsa.find('div', {'class': 'dataContent'})
		sample = tag_div_datacontent.find('table').find_all("tr")
		data = {}
		for i in sample:
			# index 1: adalah data extract untuk ukuran SALDO KUOTA (GB). 
			data[i.th.text.replace(' > ', '').replace(' ', '_').lower()] = i.find_all('td')[1].text
		
		self.__quota = data
		
	
	def myprofile(self):
		try:
			if self.__check_auth():
				# ========================
				# get object document html
				# ========================
				r = self.__session.get(Boltz.URL_PROFILE)
				html_doc = r.text
				soup = BeautifulSoup(html_doc, 'html.parser')
		
				tag_form = soup.find('form', id="selfcarechangeprofile")
				nama = tag_form.find('input', {'name': 'nama'}).get('value')
				tgl_lahir = tag_form.find('input', {'name': 'DOB'}).get('value')
				nomor_kartu_identitas = tag_form.find('input', {'name': 'nomorid'}).get('value')
				email = tag_form.find('input', {'name': 'email'}).get('value')
				submit = ''
		
				self.__profile = {
					'nama': nama,
					'tanggal_lahir': tgl_lahir,
					'nomor_id': nomor_kartu_identitas,
					'email': email,
				}
			
				if self.__check_profile():
					return True
			
				return False
			else:
				return False
		except:
			return False
			
	def get_profile(self):
		return self.__profile
	
	def __check_profile(self):
		result = True
		for k, v in self.__profile.items():
			if not v:
				result = False
		
		return result
