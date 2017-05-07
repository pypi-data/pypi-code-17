import cal
from datetime import date

def today():
	return cal.Date()

def specific_day(y,m,d,cdmy=None):
	if cdmy:
		ret = cal.Date(date(y,m,d),cal.getCDM(cdmy))
		if ret.getDays() < 0:
			return cal.Date(date(y,m,d),cal.getCDM(cdmy+1))
		return ret
	return cal.Date(date(y,m,d))
