import requests
import ConfigParser
import sys
import json
sys.path.append("..")
from apscli import apsCliConfig

class getLocalprojects:
    def __init__(self):
        self.config = apsCliConfig.apsCliConfig()
        self.local_host = self.config.getApsLocalHost()

    def getLocalMineProjectList(self):
        try:
            token = self.config.getApsLocalToken()
            url = 'http://%s/projects?mine=true'%self.local_host
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(url, headers=header)
            jsonObj = json.loads(r.text)
            if jsonObj["code"] != 0:
                print "Something wrong happened!"
                sys.exit(-1)
            project_list = jsonObj["data"]
            project_table = []
            for project in project_list:
                name = project["name"]
                project_id = project["id"]
                project_name = name + " ==> id :%s"%project_id
                project_table.append(project_name)
            for project in project_table:
                print project
            return project_list
        except requests.RequestException as e:
            print e
            sys.exit(-1)

    def getLocalProjectList(self):
        try:
            token = self.config.getApsLocalToken()
            url = 'http://%s/projects' % self.local_host
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(url, headers=header)
            jsonObj = json.loads(r.text)
            if jsonObj["code"] != 0:
                print "Something wrong happened!"
                sys.exit(-1)
            project_list = jsonObj["data"]
            project_table = []
            for project in project_list:
                name = project["name"]
                project_id = project["id"]
                project_version = project["version"]
                project_name = name + "(%s)====> id :%s" % (project_version,project_id)
                project_table.append(project_name)
            for project in project_table:
                print project
            return project_list

        except requests.RequestException as e:
            print e
            sys.exit(-1)


if __name__ == '__main__':
    a = getLocalprojects()
    a.getLocalProjectList()
