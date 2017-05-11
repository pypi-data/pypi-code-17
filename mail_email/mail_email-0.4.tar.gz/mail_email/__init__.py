#!/usr/bin/env python

import smtplib, getpass, os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

__author__  = 'hmnhGeek'
__git__     = 'https://www.github.com/hmnhGeek/mail_email/'
__version__ = 0.4

__doc__     = '''
			This module helps user to send simple mails through Python interface. User
			can also send MMS with send_MMS() feature which is fully functional now.
			  '''

def send(sender = '', receivers = [], message = '', smtp_server = 'smtp.gmail.com', port=587, pwd = ''):

	if(sender <> ''):
		server = smtplib.SMTP(smtp_server, port)
		server.ehlo()
		server.starttls()

		try:
			
			server.login(sender, pwd)
		except smtplib.SMTPAuthenticationError:
			print "Wrong Password!!"
			send(sender, receivers, smtp_server, port)

		
		server.sendmail(sender, receivers, message)
		server.close()
		print 'Message Sent!!'

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


def send_MMS(From, To, message, img_addr, Subject, password, port, server):

	'''

		Function parameters
		-------------------
			From: Sender's email address
			To:   Reciever's email address
			img_addr: Image's local address
			Subject: Email Subject
			password: Password for your email account
			port: SMTP port for your server
			server: SMTP server address

		The function sends MMS from sender's account to reciever's account.

	'''
	if(From <> ''):
		image_data = open(img_addr, 'rb').read()
		msg = MIMEMultipart()
		msg['Subject'] = Subject
		msg['From'] = From
		msg['To'] = To

		text = MIMEText(message)
		msg.attach(text)
		image = MIMEImage(image_data, name = os.path.basename(img_addr))
		msg.attach(image)

		s = smtplib.SMTP(server, port)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(From, password)
		s.sendmail(From, To, msg.as_string())
		s.quit()