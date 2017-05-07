import time
from datetime import date

def getCDM(y):
	return date(y,5,5)

def getCDMRef():
	today = date.today()
	if today.month > 5:
		return getCDM(today.year+1)
	elif today.month == 5:
		if today.day == 5:
			return today
		elif today.day > 5:
			return getCDM(today.year+1)
	return getCDM(today.year)

class Date:
	def __init__(self,normaldate=date.today(),cdm=getCDMRef()):
		t = cdm - normaldate
		self.days = t.days
		self.year = cdm.year

	def __str__(self):
		return str(self.days)+" days until Cinco de Mayo "+str(self.year)

	def __repr__(self):
		return self.__str__()

	def getDays(self):
		return self.days

	def getCDMYear(self):
		return self.year
