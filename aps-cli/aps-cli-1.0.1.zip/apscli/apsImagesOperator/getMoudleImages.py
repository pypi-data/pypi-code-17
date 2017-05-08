import os
import sys
sys.path.append("..")
import apsCliConfig

class getModuleImages:
    def __init__(self,module_name,module_id):
        print "start get module images"
        self.module_id = module_id
        self.module_name = module_name
        self.config = apsCliConfig.apsCliConfig()
        self.download_path = self.config.getApsDownloadPath()

    def getModuleImages(self):
        try:
            global images_name
            dockerfile_path = "%s/%s/Dockerfile" %(self.download_path,self.module_id)
            file = open(dockerfile_path, 'r')
            for line in file:
                a = line.split()
                if "FROM" in a:
                    images_name = a[1]
                    break
                elif "from" in a:
                    images_name = a[1]
                    break
            print images_name
            return images_name

        except Exception as e:
            print "Something wrong with getModuleImages,please check the file and try again!"
            print e
            sys.exit(-1)
