# -*- coding: utf-8 -*-

import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate
from email import encoders
from email.header import Header
import click

try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)


def send_mail(server, fro, to, subject, content, content_type='html', files=None, pics=None):
    if pics is None:
        pics = {}
    if files is None:
        files = []
    error_flag = False
    
    msg = MIMEMultipart()
    
    msg['From'] = fro
    subject = unicode(subject)
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(content, content_type, 'utf-8'))
    # print(msg)
    # print(files)
    for file in files:
        try:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment',
                            filename=u'%s'.encode('utf-8') % Header(
                                os.path.basename(file), 'utf-8'))
            
            msg.attach(part)
        except Exception as e:
            print(u'missing %s' % os.path.basename(file))
    
    for k, v in pics.items():
        fp = open(k, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', v)
        msg.attach(msgImage)
    
    import smtplib
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()
    return error_flag


@click.command()
@click.option('-t', '--title', prompt=True, default="Mail from Jmail", help='Your email title!')
@click.option('-s', '--server', prompt=True, help='Email server')
@click.option('-p', '--passwd', prompt=True, help='Your email title!')
@click.option('--sender', prompt=True, help="Sender's email address")
@click.option('--to', default=["jiajie999@gmail.com", ], help="Receiver's email address")
@click.option('--content', default="<b>Some <i>HTML</i> test text</b> and an image.<br>", help="Email's content")
@click.option('--attachs', help="Receiver's email address")
@click.option('--content_type', type=click.Choice(["html", "plan"]), default="html", help="取值:html,plain两种，默认html")
@click.option('--pics',
              help=""" 正文中图片，字典格式：{"图片路径","图片标识（eg:<imgage1>正文中使用<img src='cid:imgage1' >来引用，标识两侧尖括号不能少）"} """)
@click.option('--attachs', help="附件列表，逗号分隔多个附件")
def send(sender, to, title, content, content_type, server, passwd, attachs=None, pics=None):
    if pics is None:
        pics = {}
    if attachs is None:
        attachs = []
    elif isinstance(attachs, str):
        attachs = attachs.split(',')
        print(attachs)
    server = {'name': server, 'user': sender, 'passwd': passwd}
    print(sender, to, title, content, content_type, server, passwd, server, attachs, pics)
    # return send_mail(server, sender,
    #                  to, title, content,
    #                  content_type,
    #                  attachs, pics)
