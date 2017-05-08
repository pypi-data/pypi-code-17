#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Author: Colin
#Date: 2017-01-10
#Desc: 定义发送邮件的公共函数
#


#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Author: Colin
#Date: 2017-01-10
#Desc: 定义发送邮件的公共函数
#


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import smtplib
import os

import argparse
import logging
import datetime



## get system variables about mail
MAILHOST = os.getenv('MAILHOST')
MAILUSER = os.getenv('MAILUSER')
MAILPASSWD = os.getenv('MAILPASSWD')



def sendMail(mailto, subject, content, attachment=None):
	"""
	利用Python smtplib 模块发送邮件
	"""
	print(mailto)
	print(subject)
	print(content)
	print(attachment)

	msg = MIMEMultipart()
	# msg = MIMEText(content)


	msg['Subject'] = subject
	msg['From'] = MAILUSER
	msg['To'] = mailto
	# msg.set_charset('UTF-8')

	# attachment
	if attachment:
		print('lc-1')
		if isinstance(attachment, list):
			for afile in attachment:
				print(afile)

				realname = os.path.basename(afile)
				with open(afile, 'r') as f:
					att = MIMEText(f.read(), 'base64', 'utf-8')
					att['Content-Type'] = 'application/octet-stream'
					att['Content-Disposition'] = 'attachment; filename=' + str(realname)
					msg.attach(att)

	## content
	contenttext = MIMEText(content, 'html', 'utf-8')
	msg.attach(contenttext)

	# print(msg)
	print(type(msg))

	try:
		smtp = smtplib.SMTP()
		smtp.connect(MAILHOST)
		smtp.login(MAILUSER, MAILPASSWD)
		smtp.sendmail(MAILUSER,mailto.split(','),msg.as_string())
		smtp.close()
	except Exception as e:
		senderr=str(e)
		print(senderr)
		sendstatus=False