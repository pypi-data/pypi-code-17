#-*- coding: utf-8 -*-
import urllib 
import urllib2 
import base64, uuid,json,requests

def post(url, data): 
  req = urllib2.Request(url) 
  data = urllib.urlencode(data) 
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
  response = opener.open(req, data) 
  return response.read() 

def gettoken(API, Secret): 
  posturl = "https://openapi.baidu.com/oauth/2.0/token"
  data = {'grant_type':'client_credentials','client_id':API,'client_secret':Secret}
  token = json.loads(post(posturl, data))
  return token['access_token']

def voice(token,path):
  d = open(path, 'rb').read()
  data = {"format": "wav","rate": 16000,"channel": 1,"token": token, "cuid": ":".join([uuid.UUID(int = uuid.getnode()).hex[-12:] [e:e+2] for e in range(0,11,2)]),"len": len(d),"speech": base64.encodestring(d).replace('\n', '')}
  result = requests.post('http://vop.baidu.com/server_api', json=data, headers={'Content-Type': 'application/json'})
  data_result = result.json()
  print data_result['err_msg']
  if data_result['err_msg']=='success.':
    print "”Ô“ÙΩ·π˚£∫" + data_result['result'][0].encode('gbk')
  else:
    print data_result