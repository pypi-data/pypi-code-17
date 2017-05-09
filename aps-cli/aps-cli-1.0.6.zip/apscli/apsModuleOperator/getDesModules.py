import requests
import sys
import json
sys.path.append("..")
from apscli import apsCliConfig

class getDesModules:
    def __init__(self):
        self.config = apsCliConfig.apsCliConfig()
        self.des_host = self.config.getApsDesHost()

    def getDesModuleList(self):
        try:
            token = self.config.getApsDesToken()
            url = 'http://%s/tf/module/list'%self.des_host
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(url, headers=header)
            jsonObj = json.loads(r.text)
            if jsonObj["code"] != 0:
                print "Something wrong happened when getting target modules!"
                sys.exit(-1)
            module_list = jsonObj["data"]
            module_table = []
            for module in module_list:
                version = module["version"]
                name = module["name"]
                module_name = name + "(" + version + ")"
                module_table.append(module_name)
            for module in module_table:
                print module
            return module_list
        except Exception as e:
            print e
            sys.exit(-1)

    def getDesModuleListInfo(self):
        try:
            token = self.config.getApsDesToken()
            url = 'http://%s/tf/module/list'%self.des_host
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(url, headers=header)
            jsonObj = json.loads(r.text)
            if jsonObj["code"] != 0:
                print "Something wrong happened when getting target modules!"
                sys.exit(-1)
            module_list = jsonObj["data"]
            module_table = []
            for module in module_list:
                version = module["version"]
                name = module["name"]
                module_name = name + "(" + version + ")"
                module_table.append(module_name)
            return module_list
        except Exception as e:
            print e
            sys.exit(-1)


if __name__ == '__main__':
    a = getDesModules()
    a.getDesModuleList()

