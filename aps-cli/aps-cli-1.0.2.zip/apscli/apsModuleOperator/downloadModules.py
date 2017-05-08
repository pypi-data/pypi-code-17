import requests
import sys
import os
import apsCliConfig

class downloadModule:
    def __init__(self,module_name,module_id):
        print "perpare to download"
        self.module_name = module_name
        self.module_id = module_id
        self.config = apsCliConfig.apsCliConfig()
        self.download_path = self.config.getApsDownloadPath()
        self.local_host = self.config.getApsLocalHost()
    def downloadModule(self):
        print "downloading ......"
        try:
            os.system("mkdir -p %s/%s"%(self.download_path, self.module_id))
            base_url = 'http://%s/tf/module/download/%s'%(self.local_host,self.module_id)
            token = self.config.getApsLocalToken()
            header = {'Content-Type': 'application/json', 'X-ACCESS-TOKEN': token}
            r = requests.get(base_url,headers = header)
            tar_name = "%s-%s.tar"%(self.module_name,self.module_id)
            with open(tar_name, 'wb') as f:
                f.write(r.content)
            os.system('mv %s %s/%s/%s'%(tar_name,self.download_path, self.module_id,tar_name))
            os.system("tar -xvf %s/%s/%s -C %s/%s"%(self.download_path, self.module_id, tar_name, self.download_path, self.module_id))
            print "download successfully!!!"
        except Exception as e:
            print "something wrong with download url,please check and try again"
            print e
            sys.exit(-1)

if __name__ == '__main__':
    a = downloadModule("almodule","234")
    a.downloadModule()

