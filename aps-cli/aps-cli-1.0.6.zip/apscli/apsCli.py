import os
import ConfigParser
import apsCliMain
import apsCliConfig
import platform

def main():

    exist = os.path.exists('/usr/lib/aps-cli/config_aps.ini')
    if exist == False:
        os.system('mkdir -p /usr/lib/aps-cli')
        os.system("mkdir -p /usr/lib/aps-cli/images_list/")
        os.system("touch /usr/lib/aps-cli/images_list/images_list")
        conf = open('/usr/lib/aps-cli/config_aps.ini','w')
        config_write = ConfigParser.ConfigParser()
        config_write.add_section('config')
        config_write.set('config','local_host','')
        config_write.set('config','des_host','')
        config_write.set('config','local_token', '')
        config_write.set('config','local_cookies', '')
        config_write.set('config','des_token','')
        config_write.set('config','des_cookies','')
        config_write.set('config','download_path','/usr/lib/aps-cli')
        config_write.write(conf)
        conf.close()
        aps = apsCliMain.apsCommandLine()
        aps.main()
    else:
        aps = apsCliMain.apsCommandLine()
        aps.main()

if __name__ == '__main__':
    main()