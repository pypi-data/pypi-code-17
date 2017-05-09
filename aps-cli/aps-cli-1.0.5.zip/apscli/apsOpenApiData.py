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

class apsOpenApiHandler:
    def __init__(self):
        self.args = sys.argv[1:]
        self.config = apsCliConfig.apsCliConfig()
        self.download_path = self.config.getApsDownloadPath()
        self.des_host = self.config.getApsDesHost()

    def transferModule(self):
        parser = optparse.OptionParser()
        parser.add_option(
            "-n",
            "--name",
            dest="Module_name",
            help="input the module name you want to transfer",
            metavar="MODULE_NAME"
        )
        parser.add_option(
            "-v",
            "--version",
            dest="Version",
            help="input the module version you want to transfer",
            metavar="VERSION"
        )
        parser.add_option(
            "-i",
            "--id",
            dest="Id",
            help="input the module id you want to transfer",
            metavar="ID"
        )
        (options,self.args) = parser.parse_args()
        module_name = options.Module_name
        module_version = options.Version
        module_id = options.Id
        if module_name == None:
            print "wrong params,use --help or -h get more info"
            sys.exit(-1)
        elif module_version == None:
            print "wrong params,use --help or -h get more info"
            sys.exit(-1)
        elif module_id == None:
            print "wrong params,use --help or -h get more info"
            sys.exit(-1)
        else:
            self.transfer_one(module_name,module_version,module_id)


    def transferProject(self):
        parser = optparse.OptionParser()
        parser.add_option(
            "-i",
            "--id",
            dest="Project_id",
            help="input the project id you want to transfer",
            metavar="PROJECT_ID"
        )
        (options, args) = parser.parse_args()
        project_id = options.Project_id
        print "project_id is :"+ project_id
        if project_id == None:
            print "wrong params,use --help or -h get more info"
            sys.exit(-1)
        else:
            a = getProjectModules.getProjectModules()
            module_table = a.getProjectModules(project_id)
            b = getLocalModules.getLocalModules()
            module_list = b.getLocalModuleListInfo()
            for module in module_table:
                module_id = int(module["id"])
                print module_id
                for m in module_list:
                    if m["id"] == module_id:
                        print "starting transfer module(id:%s) ..........."%module_id
                        version = m["version"]
                        id = module_id
                        name = m["name"]
                        self.transfer_one(name,version,id)
                        print "ending transfer module(id:%s) ..........."%module_id
                    else:
                        pass

    def transfer_one(self,module_name,module_version,module_id):
        #whether the modules existing?
        a = getDesModules.getDesModules()
        des_modules = a.getDesModuleListInfo()

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
            #if the module no exist ,download the module
            down = downloadModules.downloadModule(module_name,module_id)
            down.downloadModule()
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
                print "submit %s-%s===>%s successful"%(module_name,module_version,module_id)
            except Exception as e:
                print "something wrong happened when submiting the module,please check and try again!"
                print e
        else:
            print "module already exist!"
            return 0
