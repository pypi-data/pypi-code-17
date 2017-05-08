import sys
import apsCliHelper

class apsCliParser:
    def __init__(self):
     self.args = sys.argv[1:]
     self.helper = apsCliHelper.apsCliHelper()

    def getCliCmd(self):
        if self.args.__len__() >= 1:
            return self.args[0].lower()
        else:
            self.helper.showApsCliCmdHelp()
            sys.exit(-1)
