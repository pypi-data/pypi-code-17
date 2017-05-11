import sys
import apsCliParser
import apsCliHelper
import apsOpenApiData
import apsExtensionCliHandler

class apsCommandLine:
    def __init__(self):
        self.parser = apsCliParser.apsCliParser()
        self.helper = apsCliHelper.apsCliHelper()
        self.handler = apsOpenApiData.apsOpenApiHandler()
        self.extensionHandler = apsExtensionCliHandler.apsExtensionCliHandler()
        self.args = sys.argv[1:]

    def main(self):
        cmd = self.parser.getCliCmd()
        extensionCmdList = self.extensionHandler.getAllExtensionCommands()
        if cmd in extensionCmdList:
            self.extensionHandler.handlerExtensionCmd(cmd)
        else:
            self.helper.showApsCliCmdHelp()
