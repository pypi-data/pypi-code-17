import time
import webbrowser
import random
import os
from threading import Thread
path = os.path.abspath('YT.txt')


def setPath(mypath=path) :
	path = mypath

def getInput() :
	print "What time do you want to wake up?"
	print "Use this form.\nExample: 06:30"
	Alarm = raw_input("> ")
	Time = time.strftime("%H:%M")	
	return Alarm,Time

def checkYTfile():
	#Check if the user has the YT.txt file in the same area as alarm.py
	check = True 
	if os.path.isfile("YT.txt") == False:
		print "ERROR: YT.txt file not present"
		print 'Alarm Video cannot be opened'
		check = False
	return check

def runInBackground(Time,Alarm):
	check = checkYTfile()
	with open(path) as f:
		content = f.readlines()
	while Time != Alarm:
		# print 'H'
		Time = time.strftime("%H:%M")
		time.sleep(0.95)
	# print 'Working'
	if Time == Alarm:
		# print "Time to Wake up!"
		if check :
			random_video = random.choice(content)
			webbrowser.open(random_video)
	print 'Wake UP! its ',Alarm


def runInteractive():
	check = checkYTfile()
	#The User can set the time they want to wake up. The String the user puts in must be the same as the example to work.
	Alarm,Time = getInput()
	flag = False
	ans = raw_input('Want to Run in background?(y/n)')
	thread = Thread(target=runInBackground,name='AlarmBkg',args=(Time,Alarm,))
	if ans == 'y' :
		thread.start()
	else :
		with open(path) as f:
			content = f.readlines()
		while Time != Alarm:
			os.system("clear")
			time.sleep(0.19)
			print "Alarm Time is " + Alarm
			print "The time is   " + Time
			Time = time.strftime("%H:%M")
			time.sleep(0.8)
		if Time == Alarm:
			print "Time to Wake up!"
			if check :
				random_video = random.choice(content)
				webbrowser.open(random_video)
