# -*- coding:utf-8 -*-
import io
import json
import random
import re
import sys
import thread
import time
import urllib
import xml.dom.minidom

import qrcode
import requests

from wechatbot.core import parse_command
from wechatbot.exc import BotServerException, BotErrorCode
from wechatbot.tools import create_logger

reload(sys)
sys.setdefaultencoding('utf-8')

now = lambda: int(time.time())


WECHAT_LOGIN_URL = 'https://login.weixin.qq.com/jslogin'
WECHAT_QR_CODE_STRING = 'https://login.weixin.qq.com/l/{}'
LOGIN_TEMPLATE = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s'
UPLOAD_IMG = 'https://sm.ms/api/upload'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'cache-control': 'max-age=0',
    'host': 'login.wx.qq.com',
    'content-type': 'application/json; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
}


class WechatBot(object):

    def __init__(self):

        self.session = requests.Session()

        self.uuid = None
        self.base_uri = None
        self.base_host = None

        self.skey = None
        self.sid = None
        self.uin = None
        self.pass_ticket = None
        self.device_id = 'e' + repr(random.random())[2:17]

        self.base_request = None

        self.sync_host = None
        self.sync_key = None
        self.sync_key_str = None

        self.previous_msg = ''

    def get_uuid(self):
        params = {
            'appid': 'wx782c26e4c19acffb',
            'fun': 'new',
            'lang': 'zh_CN',
            '_': int(time.time()) * 1000 + random.randint(1, 999),
        }
        r = self.session.get(WECHAT_LOGIN_URL, params=params)
        r.encoding = 'utf-8'
        data = r.text
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        pm = re.search(regx, data)
        if pm:
            code = pm.group(1)
            self.uuid = pm.group(2)
            return code == '200'
        raise BotServerException(BotErrorCode.GET_UUID_ERROR)

    def get_qr_code(self):
        string = 'https://login.weixin.qq.com/l/' + self.uuid
        img = qrcode.make(string)
        img_in_memory = io.BytesIO()
        img.save(img_in_memory, 'png')
        img_in_memory.seek(0)
        files = {'smfile': img_in_memory}
        resp = requests.post(UPLOAD_IMG, files=files)
        qr_code_url = json.loads(resp.content)['data']['url']
        hint = 'open this url to scan qrcode: {} '.format(qr_code_url)
        self.logger.info(hint)
        return qr_code_url

    def login(self):

        redirect_url = None
        tip = 1

        while not redirect_url:
            url = LOGIN_TEMPLATE % (tip, self.uuid, now())
            resp = self.session.get(url, headers=headers)

            param = re.search(r'window.code=(\d+);', resp.text)
            code = param.group(1)

            if code == '201':
                tip = 0
            elif code == '200':
                redirect_urls = re.search(r'\"(?P<redirect_url>.*)\"', resp.content)
                if redirect_urls:
                    redirect_url = redirect_urls.group('redirect_url') + '&fun=new'
                    self.base_uri = redirect_url[:redirect_url.rfind('/')]
                    temp_host = self.base_uri[8:]
                    self.base_host = temp_host[:temp_host.find("/")]
            else:
                tip = 1

        resp = self.session.get(redirect_url)

        doc = xml.dom.minidom.parseString(resp.text.encode('utf-8'))
        root = doc.documentElement

        for node in root.childNodes:
            if node.nodeName == 'skey':
                self.skey = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                self.sid = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                self.uin = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                self.pass_ticket = node.childNodes[0].data
        if all([self.skey, self.sid, self.uin, self.pass_ticket]):
            self.logger.info('bot is running...')
            return True
        raise

    def init(self):

        url = self.base_uri + '/webwxinit?r=%i&lang=en_US&pass_ticket=%s' % (now(), self.pass_ticket)
 
        self.base_request = {
            'Uin': int(self.uin),
            'Sid': self.sid,
            'Skey': self.skey,
            'DeviceID': self.device_id,
        }
 
        params = {
            'BaseRequest': self.base_request
        }
        r = self.session.post(url, data=json.dumps(params))
        dic = json.loads(r.text.encode('utf-8'))

        self.sync_key = dic['SyncKey']
        self.sync_key_str = '|'.join(str(data['Key']) + '_' + str(data['Val']) for data in self.sync_key['List'])
        if dic['BaseResponse']['Ret'] != 0:
            raise

    def sync_check(self):
        """
        sync check.
        """

        params = {
            'r': now(),
            'skey': self.skey,
            'sid': self.sid,
            'uin': self.uin,
            'deviceid': self.device_id,
            'synckey': self.sync_key_str,
            '_': now()
        }

        url = 'https://' + self.sync_host + '/cgi-bin/mmwebwx-bin/synccheck?' + urllib.urlencode(params)
        while True:
            try:
                r = self.session.get(url, timeout=20)
                r.encoding = 'utf-8'
                data = r.text
                pm = re.search(r'window.synccheck=\{retcode:"(\d+)",selector:"(\d+)"\}', data)
                retcode = pm.group(1)
                selector = pm.group(2)
                return [retcode, selector]
            except requests.exceptions.ReadTimeout:
                # This is a normal response. Just ignore this exception.
                pass
            except:
                raise

    def sync_host_check(self):
        for host1 in ['webpush.', 'webpush2.']:
            self.sync_host = host1 + self.base_host
            try:
                retcode, selector = self.sync_check()
                if retcode == '0':
                    return True
            except Exception as e:
                self.logger.error(e)
        raise

    def sync(self):
        url = self.base_uri + '/webwxsync?sid=%s&skey=%s&lang=en_US&pass_ticket=%s' % (self.sid, self.skey, self.pass_ticket)
        params = {
            'BaseRequest': self.base_request,
            'SyncKey': self.sync_key,
            'rr': ~int(time.time())
        }
        try:
            r = self.session.post(url, data=json.dumps(params), timeout=60)
            r.encoding = 'utf-8'
            dic = json.loads(r.text)
            if dic['BaseResponse']['Ret'] == 0:
                self.sync_key = dic['SyncKey']
                self.sync_key_str = '|'.join(str(data['Key']) + '_' + str(data['Val']) for data in self.sync_key['List'])
            return dic
        except Exception:
            raise

    def proc_msg(self):
        self.sync_host_check()

        while True:
            check_time = now()
            self.sync_check()
            msg = self.sync()
            try:
                self.handle_msg(msg)
            except Exception as e:
                self.logger.error(e)
            check_time = now() - check_time
            if check_time < 0.8:
                time.sleep(0.8 - check_time)

    def handle_msg(self, msgs):
        """
        """
        for msg in msgs["AddMsgList"]:
            # support group message temporally
            if ':<br/>!' in msg['Content']:
                _, msg['Content'] = msg['Content'].split('<br/>', 1)
            if not msg['Content'] or not msg['Content'].startswith('!'):
                continue
            reply = {
                'BaseRequest': self.base_request,
                'Msg': {
                    'Type': 1,
                    'Content': parse_command(msg['Content']),
                    'FromUserName': msg['ToUserName'],
                    'ToUserName': msg['FromUserName']
                },
                'Scene': msg['RecommendInfo']['Scene']
            }
            try:
                self.send_msg(reply)
            except Exception as e:
                reply['Msg']['Content'] = 'error occurs: {}'.format(e)
                self.send_msg(reply)

    def send_msg(self, reply):
        url = self.base_uri + '/webwxsendmsg'
        msg_id = str(now() * 1000) + str(random.random())[:5].replace('.', '')
        reply['Msg'].update({'LocalId': msg_id, 'ClientMsgId': msg_id})
        data = json.dumps(reply, ensure_ascii=False).encode('utf-8')
        # i haven't figured out, but you have to do this...
        # i assume, the host option is used to route. So, you have to remove host before post request
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'cache-control': 'max-age=0',
            'content-type': 'application/json; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        }
        for i in range(5):
            try:
                r = self.session.post(url, data=data, headers=headers)
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                pass
            if r.status_code == 200:
                return
        raise BotServerException(BotErrorCode.SEND_MSG_ERROR)

    @property
    def logger(self):
        """Create a logger for Bot
        """
        with thread.allocate_lock():
            return create_logger(self.__class__.__name__)

    @staticmethod
    def run():
        bot.get_uuid()
        bot.get_qr_code()
        bot.login()
        bot.init()
        bot.proc_msg()

if __name__ == "__main__":
    bot = WechatBot()
    bot.run()
