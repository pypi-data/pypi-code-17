# -*- coding: UTF-8 -*-
import os
import sys
import json
import httplib
import urllib

class RunTest():
    def __init__(self):
        pass
    def addoneVersion(self,mid):
        httpClass().AddVersion(mid)
    def uploadResult(self,caseid,retrunstr,assertstr):
        httpClass().UploadResult(caseid,retrunstr,assertstr)

class httpClass():
    web = "192.168.145.20:8088"
    #web = "localhost:8080"
    baseurl = "/testsite/runtestcaseresult";
    def __init__(self):
        pass
    def AddVersion(self,pname):
        pname=urllib.quote(pname)
        url = self.baseurl + "?action=addversion&pname=" + pname
        body = ""
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ,"Accept-Encoding":"gzip, deflate"
            ,"Accept-Language":"zh-CN,zh;q=0.8"
            ,"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
            ,"Connection":"keep-alive"
            ,"Cache-Control": "max-age=0"
            ,"Upgrade-Insecure-Requests": "1"}
        conn = httplib.HTTPConnection(self.web)  
        conn.request("GET",url=url, body=body,headers=headers)
        response = conn.getresponse()
        data = response.read()
        #print data
    def UploadResult(self,caseid,returnstr,assertstr):
        returnstr=urllib.quote(returnstr)
        url = self.baseurl + "?action=uploadresult&caseid="+caseid+"&return="+returnstr+"&assert="+assertstr
        #url = urllib.urlencode(url)
        body = ""
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                    ,"Accept-Encoding":"gzip, deflate"
                    ,"Accept-Language":"zh-CN,zh;q=0.8"
                    ,"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
                    ,"Connection":"keep-alive"
                    ,"Cache-Control": "max-age=0"
                    ,"Upgrade-Insecure-Requests": "1"}
        conn = httplib.HTTPConnection(self.web)  
        #conn.request("GET",url=url, body=body,headers=headers)
        conn.request(method="GET",url=url,headers=headers)
        response = conn.getresponse()
        data = response.read()
        #print data
    def UpLoadCase(self,data):
        url = self.baseurl
        body = MyEncoder().encode(data)
        headers = {"Content-type": "application/text"
                    , "Accept": "text/plain"}
        conn = httplib.HTTPConnection(self.web)  
        conn.request("POST",url=url, body=body,headers=headers)

        response = conn.getresponse()
        data = response.read()
        a = MyDecoder().decode(data)
        #print a["id"]
        return a

class MyEncoder(json.JSONEncoder):
    def default(self,obj):
        d = {}
        d.update(obj.__dict__)
        return d
 
class MyDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self,object_hook=self.dict2object)
    def dict2object(self,d):
        #convert dict to object
        if'__class__' in d:
            module = __import__(module_name)
            class_ = getattr(module,class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
            inst = class_(**args) #create new instance
        else:
            inst = d
        return inst