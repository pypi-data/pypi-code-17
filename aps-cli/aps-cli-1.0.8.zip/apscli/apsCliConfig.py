import sys
import os
import apsCliParser
import ConfigParser


class apsCliConfig:
    def __init__(self):
      self.args = sys.argv[1:]
      self.parser = apsCliParser.apsCliParser()

    def setApsLocalToken(self,local_token):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        fh = open('/usr/lib/aps-cli/config_aps.ini','w')
        p.set("config","local_token","%s"%local_token)
        p.write(fh)
        local_token = p.get("config","local_token")
        return local_token

    def setApsLocalCookies(self,local_cookies):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        fh = open('/usr/lib/aps-cli/config_aps.ini','w')
        p.set("config","local_cookies","%s"%local_cookies)
        p.write(fh)
        local_cookies = p.get("config","local_cookies")
        return local_cookies

    def setApsDesToken(self,des_token):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        fh = open('/usr/lib/aps-cli/config_aps.ini','w')
        p.set("config","des_token","%s"%des_token)
        p.write(fh)
        des_token = p.get("config","des_token")
        return des_token

    def setApsDesCookies(self,des_cookies):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        fh = open('/usr/lib/aps-cli/config_aps.ini','w')
        p.set("config","des_cookies","%s"%des_cookies)
        p.write(fh)
        des_cookies = p.get("config","des_cookies")
        return des_cookies

    def setApsLocalHost(self,local_host):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        fh = open('/usr/lib/aps-cli/config_aps.ini','w')
        p.set("config","local_host","%s"%local_host)
        p.write(fh)
        local_host = p.get("config","local_host")
        return local_host

    def setApsDesHost(self,des_host):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        fh = open('/usr/lib/aps-cli/config_aps.ini','w')
        p.set("config","des_host","%s"%des_host)
        p.write(fh)
        des_host = p.get("config","des_host")
        return des_host




    def getApsLocalToken(self):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        local_token = p.get("config","local_token")
        return local_token

    def getApsLocalCookies(self):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        local_cookies = p.get("config","local_cookies")
        return local_cookies

    def getApsDesToken(self):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        des_token = p.get("config","des_token")
        return des_token

    def getApsDesCookies(self):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        des_cookies = p.get("config","des_cookies")
        return des_cookies

    def getApsLocalHost(self):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        local_host = p.get("config","local_host")
        return local_host

    def getApsDesHost(self):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        des_host = p.get("config","des_host")
        return des_host

    def getApsDownloadPath(self):
        p = ConfigParser.ConfigParser()
        p.read('/usr/lib/aps-cli/config_aps.ini')
        des_host = p.get("config", "download_path")
        return des_host

