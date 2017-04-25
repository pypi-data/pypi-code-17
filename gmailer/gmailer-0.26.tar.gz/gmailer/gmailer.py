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
import pkgutil
local_settings_present = pkgutil.find_loader('local_settings')
if local_settings_present:
    from local_settings import *

def senderror(subject_text, body_text, username, password, recipients):
    """Take subject_text, body_text, username, password, recipients, send email
    
    :type subject_text: string
    :param subject_text: the subject for the email
    :type body_text: string
    :param body_text: the body for the email
    :type username: string
    :param username: the gmail username
    :type password: string
    :param password: the gmail password
    :type recipients: list
    :param recpients: list of recipients
    """

    gmailconn = gmail.GMail(username=username, password=password)
    recipients_string = ', '.join(recipients)
    msg = message.Message(subject=subject_text, to=recipients_string, text=body_text)
    gmailconn.send(msg)
    gmailconn.close()

def senderror_simple(subject_text, body_text):
    """Take subject_text and body_text and send with mail account
    NB: this function requires thatf you store in local_settings.py at the root of the python virtual machine the following (you can avoid specifying the arguments: username, password, recipients):
    import os
    #mail settings
    MAIL_CONFIG_DICT = {
        MAIL_USER='you@yourdomain.com'
        MAIL_PASS='changeme'
        MAIL_RECIPIENTS=['friend1@theirdomain.com', 'friend2@theirdoman.com']
        }
    
    :type subject_text: string
    :param subject_text: the subject for the email
    :type body_text: string
    :param body_text: the body for the email
    """
    senderror(subject_text, body_text, username=MAIL_CONFIG_DICT['MAIL_USER'], password=MAIL_CONFIG_DICT['MAIL_PASS'], recipients=MAIL_CONFIG_DICT['MAIL_RECIPIENTS'])

def senderror_attach(subject_text,body_text, username, password, recipients, attachment_file):
    """Take subject_text,body_text, username, password, recipients, attachment_file, send mail

    :type subject_text: string
    :param subject_text: the subject for the email
    :type body_text: string
    :param body_text: the body for the email
    :type attachment_file: string
    :param attachment_file: the absolute path to the attachment file
    :type username: string
    :param username: the gmail username
    :type password: string
    :param password: the gmail password
    :type recipients: list
    :param recpients: list of recipients
    """
    recipents_string = ', '.join(recipients)
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipients_string
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
    mailServer.login(username, password)
    mailServer.sendmail(username, recipients_string, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

