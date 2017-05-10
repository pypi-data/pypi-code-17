#!/usr/bin/env python

import smtplib, getpass, os

def send(sender = '', receivers = [], message = '', smtp_server = 'smtp.gmail.com', port=587):

	if(sender <> ''):
		server = smtplib.SMTP(smtp_server, port)
		server.ehlo()
		server.starttls()
		gmail_pwd = getpass.getpass("password> ")
		try:
			
			server.login(sender, gmail_pwd)
		except smtplib.SMTPAuthenticationError:
			print "Wrong Password!!"
			send(sender, receivers, smtp_server, port)

		
		server.sendmail(sender, receivers, message)
		server.close()
		print 'successfully sent the mail'

def write_mail():
	os.system('subl message.txt')


def make_recievers(data):
	recv = ''
	brackets = []
	for i in data:

		if('[' in i and ']' in i):
			return i
		else:
			if(brackets <> ['[', ']']):
				if '[' in i:
					brackets.append('[')
					recv += i
				else:
					if '[' in brackets and ']' not in brackets:
						if ']' in i:
							brackets.append(']')
							recv += i
							return recv
						else:
							recv += i


