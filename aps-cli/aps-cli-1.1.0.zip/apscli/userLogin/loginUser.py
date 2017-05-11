import json
import requests
import sys
sys.path.append("..")
from apscli import apsCliConfig

class loginUser:
    def __init__(self):
        print "logining user ......"
        self.config = apsCliConfig.apsCliConfig()
        self.local_host = self.config.getApsLocalHost()
        self.des_host = self.config.getApsDesHost()

    def loginLocalUser(self,local_user,local_pwd):
        try:
            jsonObj = {'account': local_user, 'password': local_pwd}
            data = json.dumps(jsonObj)
            url = 'http://%s/user/login' % self.local_host
            header = {'Content-Type': 'application/json'}
            r = requests.post(url, data=data, headers=header)
            a = r.cookies.get_dict().get('express:sess')
            b = r.cookies.get_dict().get('express:sess.sig')
            try:
                _cookies = 'express:sess=' + a + ';express:sess.sig=' + b + ';'
                print 'login success!'
                s = json.loads(r.text)
                token = s['data']['token']
                info_list = []
                info_list.append(token)
                info_list.append(_cookies)
                return info_list
            except:
                print 'please input right local message!'
                sys.exit(-1)
        except requests.RequestException as e:
            print e
            sys.exit(-1)

    def loginTargetUser(self,des_user,des_pwd):
        try:
            jsonObj = {'account': des_user, 'password': des_pwd}
            data = json.dumps(jsonObj)
            url = 'http://%s/user/login' % self.des_host
            header = {'Content-Type': 'application/json'}
            r = requests.post(url, data=data, headers=header)
            a = r.cookies.get_dict().get('express:sess')
            b = r.cookies.get_dict().get('express:sess.sig')
            try:
                _cookies = 'express:sess=' + a + ';express:sess.sig=' + b + ';'
                print 'login success!'
                s = json.loads(r.text)
                token = s['data']['token']
                info_list = []
                info_list.append(token)
                info_list.append(_cookies)
                return info_list
            except:
                print 'please input right target message!'
                sys.exit(-1)
        except requests.RequestException as e:
            print e
            sys.exit(-1)

