import requests
import sys
import json
sys.path.append("..")
import apsCliConfig

class getLocalModules:
    def __init__(self):
        self.config = apsCliConfig.apsCliConfig()
        self.local_host = self.config.getApsLocalHost()

    def getLocalModuleList(self):
        try:
            token = self.config.getApsLocalToken()
            url = 'http://%s/tf/module/list'%self.local_host
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(url, headers=header)
            jsonObj = json.loads(r.text)
            if jsonObj["code"] != 0:
                print "Something wrong happened!"
                sys.exit(-1)
            module_list = jsonObj["data"]
            module_table = []
            for module in module_list:
                version = module["version"]
                name = module["name"]
                module_id = module["id"]
                module_name = name + "(" + version + ")========>id : %s"%module_id
                module_table.append(module_name)
            for module in module_table:
                print module
            return module_list
        except Exception as e:
            print e
            sys.exit(-1)

    def getLocalModuleListInfo(self):
        try:
            token = self.config.getApsLocalToken()
            url = 'http://%s/tf/module/list'%self.local_host
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(url, headers=header)
            jsonObj = json.loads(r.text)
            if jsonObj["code"] != 0:
                print "Something wrong happened!"
                sys.exit(-1)
            module_list = jsonObj["data"]
            module_table = []
            for module in module_list:
                version = module["version"]
                name = module["name"]
                module_id = module["id"]
                module_name = name + "(" + version + ")========>id : %s"%module_id
                module_table.append(module_name)
            return module_list
        except Exception as e:
            print e
            sys.exit(-1)


if __name__ == '__main__':
    a = getLocalModules()
    a.getLocalModuleList()
