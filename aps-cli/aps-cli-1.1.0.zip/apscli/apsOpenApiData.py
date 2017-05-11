import sys
import optparse
import os
import apsCliConfig
from apsModuleOperator import getLocalModules
from apsModuleOperator import getDesModules
from apsImagesOperator import getMoudleImages
from apsImagesOperator import getDesImages
from apsModuleOperator import downloadModules
from apsProjetcOperator import getProjects
from apsModuleOperator import getProjectModules
from userLogin import loginUser

class apsOpenApiHandler:
    def __init__(self):
        self.args = sys.argv[1:]
        self.config = apsCliConfig.apsCliConfig()
        self.download_path = self.config.getApsDownloadPath()
        self.des_host = self.config.getApsDesHost()
        self.local_host = self.config.getApsLocalHost()
        self.login = loginUser.loginUser()

    def listLocalModules(self):
        parser = optparse.OptionParser()
        parser.add_option(
            "-u",
            "--user",
            dest="User",
            help="input the local username",
            metavar="User"
        )
        parser.add_option(
            "-p",
            "--password",
            dest="Password",
            help="input the local user password",
            metavar="Password"
        )
        (options, self.args) = parser.parse_args()
        local_user = options.User
        local_password = options.Password
        if local_user == None:
            print "local username can't be NONE"
            sys.exit(-1)
        if local_password == None:
            print "local password can't be None"
            sys.exit(-1)
        user_info = self.login.loginLocalUser(local_user,local_password)
        try:
            local_token = user_info[0]
            local_cookies = user_info[1]
            a = getLocalModules.getLocalModules()
            a.getLocalModuleList(local_token)
        except Exception as e:
            print "login failed , please try again!"
            sys.exit(-1)

    def listLocalProjects(self):
        parser = optparse.OptionParser()
        parser.add_option(
            "-u",
            "--user",
            dest="User",
            help="input the local username",
            metavar="User"
        )
        parser.add_option(
            "-p",
            "--password",
            dest="Password",
            help="input the local user password",
            metavar="Password"
        )
        (options, self.args) = parser.parse_args()
        local_user = options.User
        local_password = options.Password
        if local_user == None:
            print "local username can't be NONE"
            sys.exit(-1)
        if local_password == None:
            print "local password can't be None"
            sys.exit(-1)
        user_info = self.login.loginLocalUser(local_user, local_password)
        try:
            local_token = user_info[0]
            local_cookies = user_info[1]
            a = getProjects.getLocalprojects()
            a.getLocalProjectList(local_token)
        except Exception as e:
            print "login failed , please try again!"
            sys.exit(-1)

    def listTargetModules(self):
        parser = optparse.OptionParser()
        parser.add_option(
            "-u",
            "--user",
            dest="User",
            help="input the target username",
            metavar="User"
        )
        parser.add_option(
            "-p",
            "--password",
            dest="Password",
            help="input the target user password",
            metavar="Password"
        )
        (options, self.args) = parser.parse_args()
        target_user = options.User
        target_password = options.Password
        if target_user == None:
            print "target username can't be NONE"
            sys.exit(-1)
        if target_password == None:
            print "target password can't be None"
            sys.exit(-1)
        user_info = self.login.loginTargetUser(target_user,target_password)
        try:
            des_token = user_info[0]
            des_cookies = user_info[1]
            a = getDesModules.getDesModules()
            a.getDesModuleList(des_token)
        except Exception as e:
            print "login failed , please try again!"
            sys.exit(-1)

    def transferModule(self):
        parser = optparse.OptionParser()
        parser.add_option(
            "-i",
            "--id",
            dest="Id",
            help="input the module id you want to transfer",
            metavar="ID"
        )
        parser.add_option(
            "-u",
            "--local_user",
            dest="Local_user",
            help="input the local username",
            metavar="LOCAL_USER"
        )
        parser.add_option(
            "-p",
            "--local_password",
            dest="Local_password",
            help="input the local user password",
            metavar="LOCAL_PASSWORD"
        )
        parser.add_option(
            "-n",
            "--target_user",
            dest="Target_user",
            help="input the target username",
            metavar="TARGET_USER"
        )
        parser.add_option(
            "-d",
            "--target_password",
            dest="Target_password",
            help="input the target user password",
            metavar="TARGET_PASSWORD"
        )
        (options,self.args) = parser.parse_args()
        module_id = options.Id
        local_user = options.Local_user
        local_password = options.Local_password
        target_user = options.Target_user
        target_password = options.Target_password

        if local_user == None:
            print "local username can't be NONE"
            sys.exit(-1)
        if local_password == None:
            print "local password can't be None"
            sys.exit(-1)
        if target_user == None:
            print "target username can't be NONE"
            sys.exit(-1)
        if target_password == None:
            print "target password can't be None"
            sys.exit(-1)
        if module_id == None:
            print "wrong params,use --help or -h get more info"
            sys.exit(-1)
        else:
            local_info = self.login.loginLocalUser(local_user,local_password)
            target_info = self.login.loginTargetUser(target_user,target_password)
            local_token = local_info[0]
            local_cookies = local_info[1]
            target_token = target_info[0]
            target_cookies = target_info[1]
            lo = getLocalModules.getLocalModules()
            local_modules = lo.getLocalModuleListInfo(local_token)
            for module in local_modules:
                if int(module_id) == module["id"]:
                    module_name = module["name"]
                    module_version = module["version"]
                    self.transfer_one(module_name,module_version,module_id,local_token,target_token)
                    break
                else:
                    pass
            print "end transfer module"


    def transferProject(self):
        parser = optparse.OptionParser()
        parser.add_option(
            "-i",
            "--id",
            dest="Project_id",
            help="input the project id you want to transfer",
            metavar="PROJECT_ID"
        )
        parser.add_option(
            "-u",
            "--local_user",
            dest="Local_user",
            help="input the local username",
            metavar="LOCAL_USER"
        )
        parser.add_option(
            "-p",
            "--local_password",
            dest="Local_password",
            help="input the local user password",
            metavar="LOCAL_PASSWORD"
        )
        parser.add_option(
            "-n",
            "--target_user",
            dest="Target_user",
            help="input the target username",
            metavar="TARGET_USER"
        )
        parser.add_option(
            "-d",
            "--target_password",
            dest="Target_password",
            help="input the target user password",
            metavar="TARGET_PASSWORD"
        )
        (options, args) = parser.parse_args()
        project_id = options.Project_id
        local_user = options.Local_user
        local_password = options.Local_password
        target_user = options.Target_user
        target_password = options.Target_password

        if local_user == None:
            print "local username can't be NONE"
            sys.exit(-1)
        if local_password == None:
            print "local password can't be None"
            sys.exit(-1)
        if target_user == None:
            print "target username can't be NONE"
            sys.exit(-1)
        if target_password == None:
            print "target password can't be None"
            sys.exit(-1)
        if project_id == None:
            print "wrong params,use --help or -h get more info"
            sys.exit(-1)
        else:
            local_info = self.login.loginLocalUser(local_user, local_password)
            target_info = self.login.loginTargetUser(target_user, target_password)
            local_token = local_info[0]
            local_cookies = local_info[1]
            target_token = target_info[0]
            target_cookies = target_info[1]
            a = getProjectModules.getProjectModules()
            module_table = a.getProjectModules(project_id,local_token)
            b = getLocalModules.getLocalModules()
            module_list = b.getLocalModuleListInfo(local_token)
            for module in module_table:
                module_id = int(module["id"])
                print module_id
                for m in module_list:
                    if m["id"] == module_id:
                        print "starting transfer module(id:%s) ..........."%module_id
                        version = m["version"]
                        id = module_id
                        name = m["name"]
                        self.transfer_one(name,version,id,local_token,target_token)
                        print "ending transfer module(id:%s) ..........."%module_id
                    else:
                        pass

    def transfer_one(self,module_name,module_version,module_id,local_token,target_token):
        #whether the modules existing?
        a = getDesModules.getDesModules()
        des_modules = a.getDesModuleListInfo(target_token)

        global sign
        sign = 0
        for module in des_modules:
            if module["name"] == module_name and module["version"] == module_version:
                print "The module already exist"
                sign = 1
                break
            else:
                pass
        if sign == 0:
            lo = getLocalModules.getLocalModules()
            local_modules = lo.getLocalModuleListInfo(local_token)
            id_list = []
            for module in local_modules:
                id = module["id"]
                id_list.append(id)
            if module_id in id_list:
                #if the module no exist ,download the module
                down = downloadModules.downloadModule(module_name,module_id)
                down.downloadModule(local_token)
                #get the module's dockfile info
                lname = getMoudleImages.getModuleImages(module_name,module_id)
                image_name = lname.getModuleImages()
                #get the target server's images info,if already exist,don't need to load images
                images = getDesImages.getDesImages()
                des_images_list = images.getDesImagesInfo()
                if image_name in des_images_list:
                    print "the dockerfile's images already exist in the target server....."
                    print "coutinue"
                else:
                    print "start saving docker images"
                    try:
                        os.system("docker save %s > %s/%s/%s"%(image_name,self.download_path,module_id,module_name))
                        print "successfully saved docker images"
                    except Exception as e:
                        print "save images failed"
                        print "wrong Info :",e
                        sys.exit(-1)
                #copy the module file to the target server
                os.system("ssh -n root@%s 'mkdir -p %s'"%(self.des_host,self.download_path))
                os.system("scp -r %s/%s root@%s:%s"%(self.download_path,module_id,self.des_host,self.download_path))
                #submit the module
                try:
                    if image_name not in des_images_list:
                        os.system("ssh -n root@%s 'docker load < %s/%s/%s'"%(self.des_host,self.download_path,module_id,module_name))
                        os.system("ssh -n root@%s 'cd %s/%s && screwjack submit'"%(self.des_host,self.download_path,module_id))
                    else:
                        os.system("ssh -n root@%s 'cd %s/%s && screwjack submit'" % (self.des_host, self.download_path, module_id))
                    print "submit %s-%s===>%s"%(module_name,module_version,module_id)
                except Exception as e:
                    print "something wrong happened when submiting the module,please check and try again!"
                    print e
            else:
                print "the module id doesn't exist!"
                return 0
        else:
            print "module already exist!"
            return 0
