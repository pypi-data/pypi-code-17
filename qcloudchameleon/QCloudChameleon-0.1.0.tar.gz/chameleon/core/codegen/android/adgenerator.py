from ..model import *
from ..property import *
from mako.template import Template
from mako.lookup import TemplateLookup
from ...utilities.constant import OCOutType
from ...config.config import *
import codecs
import os

class AndroidGenerator(object):
    """docstring for AndroidGenerator."""
    def __init__(self, model, outPath, template):
        super(AndroidGenerator, self).__init__()
        self.model = model
        self.outPath = outPath
        if template == None:
            template = Config.APP_BIN_PATH+"/../resources/template/android/model"
        self.tlLookup = TemplateLookup(directories=template)
        pass


    def outPutFileName(self):
        return self.model.name

    def renderFileContent(self, file):
        fileTl = self.tlLookup.get_template(file)
        content = fileTl.render(model=self.model)
        return content

    def outputFileWithRender(self, filename, tlname, overwrite):
        filePath = os.path.join(self.outPath, filename)
        if overwrite and  os.path.exists(filePath):
            return
        content = self.renderFileContent(tlname)
        f = codecs.open(filePath, "w+", "utf-8")
        f.write(content)
        f.close()

    def output(self, overwrite):
        if os.path.exists(self.outPath) == False:
            os.mkdir(self.outPath)
        fileName = self.outPutFileName() + ".java"
        self.outputFileWithRender(fileName,"model.clout", overwrite)
        pass

class AndroidRequestGenerator(AndroidGenerator):
    """docstring for AndroidRequestGenerator."""
    def __init__(self, model, outPath, template):
        super(AndroidRequestGenerator, self).__init__(model, outPath, template)
        if template == None:
            template = Config.APP_BIN_PATH+"/../resources/template/android/request"
        self.tlLookup = TemplateLookup(directories=template)
