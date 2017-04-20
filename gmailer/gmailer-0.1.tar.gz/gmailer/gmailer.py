#!/usr/bin/env python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
from gmail import gmail
from gmail import message
import sys
import vmtools

vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
from local_settings import *


def senderror(subject_text, body_text):
    """Take subject_text and body_text and send with gmail account stored in local_settings.py
    i.e:
    #gmail settings
    GMAIL_USER=''
    GMAIL_PASS=''

    :type subject_text: string
    :param subject_text: the subject for the email
    :type body_text: string
    :param body_text: the body for the email
    """

    gmailconn = gmail.GMail(username=GMAIL_USER, password=GMAIL_PASS)
    msg = message.Message(subject=subject_text, to=ERROR_RECIPIENT, text=body_text)
    gmailconn.send(msg)
    gmailconn.close()



def senderror_attach(subject_text,body_text, attachment_file):
    """Take subject_text, body_text, and attachment_file and send with gmail account store in local_settings.py
    i.e:
    #gmail settings
    GMAIL_USER=''
    GMAIL_PASS=''

    :type subject_text: string
    :param subject_text: the subject for the email
    :type body_text: string
    :param body_text: the body for the email
    :type attachment_file: string
    :param attachment_file: the absolute path to the attachment file
    """
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = ERROR_RECIPIENT
    msg['Subject'] = subject_text
 
    msg.attach(MIMEText(body_text))
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachment_file, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
            'attachment; filename="%s"' % os.path.basename(attachment_file))
    msg.attach(part)
 
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(GMAIL_USER, GMAIL_PASS)
    mailServer.sendmail(GMAIL_USER, ERROR_RECIPIENT, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

