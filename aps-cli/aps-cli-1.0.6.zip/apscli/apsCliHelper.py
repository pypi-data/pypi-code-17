import platform
import ConfigParser

class apsCliHelper:
    class color:
      if platform.system() == "Windows":
        purple = ''
        cyan = ''
        blue = ''
        green = ''
        yellow = ''
        red  = ''
        bold = ''
        underline = ''
        end = ''
      else:
        purple = '\033[95m'
        cyan = '\033[96m'
        blue = '\033[94m'
        green = '\033[92m'
        yellow = '\033[93m'
        red  = '\033[91m'
        bold = '\033[1m'
        underline = '\033[4m'
        end = '\033[0m'

    def showApsCliCmdHelp(self):
        print self.color.bold+"NAME:"+self.color.end
        print "aps-cli "
        print self.color.bold+"\nDESCRIPTION:"+self.color.end
        print "You can get local projects and you can also transfer local modules to a target server"
        print self.color.bold+"SYNOPSIS\n"+self.color.end
        print "aps-cli <operation> [options and parameters]"
        print "before use the cli,you must write necessary config info into our configure file(local_host,des_host)"
        print "The configure file path is : /usr/lib/aps-cli/config_aps.ini"
        print ""
        print "login to the local datacanvas and target datacanvas is also necessary,you can use the commands before:"
        print self.color.bold + "o login_local_user" +self.color.end
        print self.color.bold + "o login_target_user" + self.color.end
        print '---------------make sure you have already did the things behind,you can use the cmd below-----------------------------------------'
        print self.color.bold + "The commands: "+self.color.end
        print self.color.bold + "o list_local_projects" +self.color.end
        print self.color.bold + "o list_local_modules" +self.color.end
        print self.color.bold + "o list_target_modules" + self.color.end
        print self.color.bold + "o list_target_images" + self.color.end
        print self.color.bold + "o transmodule     =>  You can use this command transfer a local module the target server!" + self.color.end
        print self.color.bold + "o transproject    =>  You can use this command transfer several modules which a project include to the target server!" + self.color.end
