import cal,sys
from datetime import date

def cdmdate():
	today = cal.Date()
	print("Today is "+str(today)+".")

def cdmdateconv():
	if len(sys.argv)!=4:
		print("Usage: cdmdateconv <year> <month> <date>")
		return 1
	args = [int(s) for s in sys.argv[1:]]
	day = cal.Date(date(*args),cal.getCDM(args[0]))
	if day.getDays() < 0:
		day = cal.Date(date(*args),cal.getCDM(args[0]+1))
	print("{!s}-{!s}-{!s} is {!s}".format(args[0],args[1],args[2],day))
