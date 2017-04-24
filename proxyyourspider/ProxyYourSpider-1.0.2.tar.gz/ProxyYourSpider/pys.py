# -*- encoding:utf-8 -*-

import time
import redis
import requests
import threading
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

offset = 0

class Proxy(object):
    llen = 0
    size = 0
    url = "http://proxydb.net/?protocol=http&protocol=https&anonlvl=4" 
    http_test_url = 'http://httpbin.org/ip'
    https_test_url = 'https://httpbin.org/ip'

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def fillProxyPool(self):
        global offset
        while self.llen < self.size:
            url = self.url + '&offset=' + str(offset)
            offset += 50
            ua = UserAgent()
            headers = {'User-Agent' : ua.random}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            lists = soup.find('tbody').find_all('tr')
            for ls in lists:
                tds = ls.find_all('td')
                proxy = ''.join(tds[0].text.split())
                _type = ''.join(tds[1].text.split()).lower()
                validity = self.checkValidity(_type, proxy)
                if validity == True:
                    self.r.lpush(_type, proxy)
                    print '1 proxy added: %s. http: %d; https: %s.' \
                            %(proxy, self.r.llen('http'), self.r.llen('https'))
            self.__class__.llen += self.r.llen('http') + self.r.llen('https')

    def checkValidity(self, _type, proxy):
        proxyDict = {_type : _type + '://' + proxy}
        ua = UserAgent()
        headers = {'User-Agent' : ua.random}
        try:
            if _type == 'http':
                r = requests.get(self.http_test_url, proxies=proxyDict,\
                        headers=headers, timeout=1)
            else:
                r = requests.get(self.https_test_url, proxies=proxyDict,\
                        headers=headers, timeout=2)
        except Exception:
            return False
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            retDict = eval(soup.find('body').text)
        except Exception:
            return False
        if proxy.split(':')[0] == retDict['origin']:
            return True
    
    def createProxyPool(self, size):
        self.__class__.size = size
        t1 = threading.Thread(target=self.fillProxyPool)
        t2 = threading.Thread(target=self.fillProxyPool)
        t3 = threading.Thread(target=self.fillProxyPool)
        t4 = threading.Thread(target=self.fillProxyPool)
        t5 = threading.Thread(target=self.fillProxyPool)
        t6 = threading.Thread(target=self.fillProxyPool)
        t7 = threading.Thread(target=self.fillProxyPool)
        t8 = threading.Thread(target=self.fillProxyPool)
        t9 = threading.Thread(target=self.fillProxyPool)
        t10 = threading.Thread(target=self.fillProxyPool)
        t11 = threading.Thread(target=self.fillProxyPool)
        t12 = threading.Thread(target=self.fillProxyPool)
        t13 = threading.Thread(target=self.fillProxyPool)
        t14 = threading.Thread(target=self.fillProxyPool)
        t15 = threading.Thread(target=self.fillProxyPool)
        t16 = threading.Thread(target=self.fillProxyPool)
        t1.start()
        time.sleep(1)
        t2.start()
        time.sleep(1)
        t3.start()
        time.sleep(1)
        t4.start()
        time.sleep(1)
        t5.start()
        time.sleep(1)
        t6.start()
        time.sleep(1)
        t7.start()
        time.sleep(1)
        t8.start()
	time.sleep(1)
        t9.start()
        time.sleep(1)
        t10.start()
        time.sleep(1)
        t11.start()
        time.sleep(1)
        t12.start()
        time.sleep(1)
        t13.start()
        time.sleep(1)
        t14.start()
        time.sleep(1)
        t15.start()
        time.sleep(1)
        t16.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()
        t11.join()
        t12.join()
        t13.join()
        t14.join()
        t15.join()
        t16.join()
        return (self.r.llen('http'), self.r.llen('https'))

    def fetchProxy(self, _type):
        while True:
            proxy = self.r.lpop(_type)
            validity = self.checkValidity(_type, proxy)
            if validity == True:
                self.r.rpush(_type, proxy)
                break
            else:
                self.llen -= 1
        return (_type, proxy)
    
    def autoUpdate(self):
        while True:
            self.fillProxyPool()
            time.sleep(10)
            print "update..."
