import sys
import apsCliParser
import apsCliHelper
import apsOpenApiData
import json
import requests
import getpass
import ConfigParser
import apsCliConfig
from apsModuleOperator import getDesModules
from apsModuleOperator import getLocalModules
from apsImagesOperator import getDesImages
from apsProjetcOperator import getProjects


class apsExtensionCliHandler:
    def __init__(self):
        self.parser = apsCliParser.apsCliParser()
        self.helper = apsCliHelper.apsCliHelper()
        self.config = apsCliConfig.apsCliConfig()

    def getAllExtensionCommands(self):
        cmdList = ['-h','--help','login_local_user','login_target_user','list_local_modules','list_target_modules','list_local_projects','list_target_images','transmodule','transproject']
        return cmdList

    def handlerExtensionCmd(self,cmd):
        if cmd in ['help', '-h', '--help']:
            self.helper.showApsCliCmdHelp()
        elif cmd == "login_local_user":
            name = raw_input('Your local username:')
            password = getpass.getpass('Your local password:')
            try:
                jsonObj = {'account': name, 'password': password}
                data = json.dumps(jsonObj)
                local_host = self.config.getApsLocalHost()

                url = 'http://%s/user/login' % (local_host)
                header = {'Content-Type': 'application/json'}
                r = requests.post(url, data=data, headers=header)
                a = r.cookies.get_dict().get('express:sess')
                b = r.cookies.get_dict().get('express:sess.sig')
                try:
                    _cookies = 'express:sess=' + a + ';express:sess.sig=' + b + ';'
                    self.config.setApsLocalCookies(_cookies)
                    print 'login success!'
                    s = json.loads(r.text)
                    token = s['data']['token']
                    self.config.setApsLocalToken(token)
                except:
                    print 'please input right message!'
            except requests.RequestException as e:
                print e
                sys.exit(-1)

        elif cmd == "login_target_user":
            name = raw_input('Your target username:')
            password = getpass.getpass('Your target password:')
            try:
                jsonObj = {'account': name, 'password': password}
                data = json.dumps(jsonObj)
                des_host = self.config.getApsDesHost()

                url = 'http://%s/user/login' % (des_host)
                header = {'Content-Type': 'application/json'}
                r = requests.post(url, data=data, headers=header)
                a = r.cookies.get_dict().get('express:sess')
                b = r.cookies.get_dict().get('express:sess.sig')
                try:
                    _cookies = 'express:sess=' + a + ';express:sess.sig=' + b + ';'
                    self.config.setApsDesCookies(_cookies)
                    print 'login success!'
                    s = json.loads(r.text)
                    token = s['data']['token']
                    self.config.setApsDesToken(token)
                except:
                    print 'please input right message!'
            except requests.RequestException as e:
                print e
                sys.exit(-1)

        elif cmd == "list_local_modules":
            try:
                a = getLocalModules.getLocalModules()
                a.getLocalModuleList()
            except Exception as e:
                print "get local_modules_list failed"
                print e

        elif cmd == "list_target_modules":
            try:
                a = getDesModules.getDesModules()
                a.getDesModuleList()
            except Exception as e:
                print "get target_modules_list failed"
                print e

        elif cmd == "list_local_projects":
            try:
                a = getProjects.getLocalprojects()
                a.getLocalProjectList()
            except Exception as e:
                print "get target_projects_list failed"
                print e

        elif cmd == "list_target_images":
            try:
                a = getDesImages.getDesImages()
                a.getDesImages()
            except Exception as e:
                print "get target_images_list failed"
                print e

        elif cmd == "transmodule":
            try:
                a = apsOpenApiData.apsOpenApiHandler()
                a.transferModule()
            except Exception as e:
                print "something wrong happened when transfor module"
                print "please use -h or --help to get more information"
                print e

        elif cmd == "transproject":
            try:
                a = apsOpenApiData.apsOpenApiHandler()
                a.transferProject()
            except Exception as e:
                print "something wrong happened when transfor project"
                print "please use -h or --help to get more information"
                print e

        else:
            self.helper.showApsCliCmdHelp()
