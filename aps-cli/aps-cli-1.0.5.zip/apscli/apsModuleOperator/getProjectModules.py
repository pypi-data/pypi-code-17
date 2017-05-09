import requests
import sys
import json
sys.path.append("..")
from apscli import apsCliConfig

class getProjectModules:
    def __init__(self):
        self.config = apsCliConfig.apsCliConfig()
        self.local_host = self.config.getApsLocalHost()

    def getProjectModules(self,project_id):
        try:
            token = self.config.getApsLocalToken()
            url = 'http://%s/projects/workspaceinfo/%s'%(self.local_host,project_id)
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(url, headers=header)
            jsonObj = json.loads(r.text)
            if jsonObj["code"] != 0:
                print "Something wrong happened!"
                sys.exit(-1)
            module_list = jsonObj["data"]["locations"]
            module_table = []
            module_id_table = []
            for module in module_list:
                module_id = module["moduleId"]
                if module_id not in module_id_table:
                    if int(module["moduleType"]) == 0:
                        module_id_table.append(module_id)
                        module_name = module["name"]
                        module_info = {"name":module_name,"id":module_id}
                        module_table.append(module_info)
                        print "module_id:%s=====>id:%s"%(module_name,module_id)
                    else:
                        print "module_id:%s is a data module"%module_id
                else:
                    print "module_id:%s is a same module in project"%module_id
            return module_table

        except requests.RequestException as e:
            print e
            sys.exit(-1)

if __name__ == '__main__':
    a = getProjectModules()
    a.getProjectModules(804)
