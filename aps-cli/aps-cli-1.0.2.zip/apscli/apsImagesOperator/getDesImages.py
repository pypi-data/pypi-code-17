import os
import sys
import apsCliConfig

class getDesImages:
    def __init__(self):
        print "start get target existing images"
        self.config = apsCliConfig.apsCliConfig()
        self.des_host = self.config.getApsDesHost()

    def getDesImages(self):
        try:
            command = "ssh -n root@%s 'docker images' > /usr/lib/aps-cli/images_list/images_list"%self.des_host
            os.system(command)
            file = open("/usr/lib/aps-cli/images_list/images_list")
            global i
            i = 0
            images_list = []
            for line in file:
                if i == 0:
                    i = i + 1
                else:
                    a = line.split()
                    image_name = a[0]
                    image_version = a[1]
                    image_name = "%s:%s"%(image_name,image_version)
                    images_list.append(image_name)
            for images in images_list:
                print images
            return images_list

        except Exception as e:
            print "something wrong happened when get the target images"
            print e
            sys.exit(-1)

    def getDesImagesInfo(self):
        try:
            command = "ssh -n root@%s 'docker images' > /usr/lib/aps-cli/images_list/images_list" % self.des_host
            os.system(command)
            file = open("/usr/lib/aps-cli/images_list/images_list")
            global i
            i = 0
            images_list = []
            for line in file:
                if i == 0:
                    i = i + 1
                else:
                    a = line.split()
                    image_name = a[0]
                    image_version = a[1]
                    image_name = "%s:%s" % (image_name, image_version)
                    images_list.append(image_name)
            return images_list

        except Exception as e:
            print "something wrong happened when get the target images"
            print e
            sys.exit(-1)