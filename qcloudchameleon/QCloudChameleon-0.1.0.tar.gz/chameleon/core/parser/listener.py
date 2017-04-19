# coding: UTF-8
from ..engine.ChameleonListener import *
from ..codegen.model import *
from ..codegen.request import *

from ..codegen.property import  PropertyFactory
from ..codegen.property import NSArrayProperty
from ..codegen.oc.generate import *
from ..codegen.android.adgenerator import *
from ..config.config import *
from ..utilities.constant import *

class CLBuildListener(ChameleonListener):
    pass
    def __init__(self):
        ChameleonListener.__init__(self)
        self.models = []
        pass

    def enterProg(self, ctx):
        pass

    def exitProg(self, ctx):
        pass

    def topModel(self):
        if len(self.models) < 1 :
           return  None
        return self.models[-1]
    def loadPropertyParamters(self, property, ctx):
        data = ctx.request_paramters()
        if data == None or len(data) == 0:
            print("NULL paramters")
            return
        print("%s" % (data))
        data = data[0]
        data = data.ID()
        print("type is %s" % type(data))
        if len(data)>0:
            for p in data:
                paramter = p.getText()
                property.addParamter(paramter)

    def exitC_property_name(self, ctx):
        name = ctx.ID().getText();
        type = ctx.p_type().getText()
        p = PropertyFactory(name, type)
        assert(p)
        model = self.topModel()
        self.loadPropertyParamters(p, ctx)
        model.addProperty(p)
        pass

    def exitC_property_second_name(self, ctx):
        name = ctx.ID(0).getText()
        secondName = ctx.ID(1).getText()
        type = ctx.p_type().getText()
        p = PropertyFactory(name, type, secondName)
        assert(p)
        self.loadPropertyParamters(p, ctx)
        model = self.topModel()
        model.addProperty(p)
        pass

    def exitArray_property_name(self, ctx):
        name = ctx.ID().getText()
        type = ctx.p_type().getText()
        p = NSArrayProperty(name, type)
        assert(p)
        model = self.topModel()
        self.loadPropertyParamters(p, ctx)
        model.addProperty(p)
        pass

    def exitArray_property_second_name(self, ctx):
        name = ctx.ID(0).getText()
        secondName = ctx.ID(1).getText()
        type = ctx.p_type().getText()
        p = NSArrayProperty(name, type, secondName)
        assert(p)
        model = self.topModel()
        self.loadPropertyParamters(p, ctx)
        model.addProperty(p)
        pass

    def enterModel(self, ctx):
        name =  ctx.ID().getText()
        model = OCModel(name)
        self.models.append(model)
        pass

    def enterRequest_paramters(self, ctx):

        pass

        # Exit a parse tree produced by ChameleonParser#request_paramters.
    def exitRequest_paramters(self, ctx):
        pass
    def exitModel(self, ctx):
        model = self.topModel()
        generator = None
        if Config.LUANGUAGE_TYPE == LanguageType.Objective_C:
            generator = OCGenerator(model, Config.OUTPUT_DIR, Config.OC_TYPE, Config.TEMPLATE)
        elif Config.LUANGUAGE_TYPE == LanguageType.Android:
            generator = AndroidGenerator(model, Config.OUTPUT_DIR,None)
        generator.output(True)
        pass

    # Enter a parse tree produced by ChameleonParser#request.
    def enterRequest(self, ctx):
        name = ctx.ID().getText()
        request = OCRequestModel(name)
        self.models.append(request)

        data = ctx.request_paramters()
        if data == None or len(data) == 0:
            print("NULL paramters")
            return
        print("%s" % (data))
        data = data[0]
        data = data.ID()
        if len(data)>0:
            model = request
            if not isinstance(model, OCRequestModel):
                return
            for p in data:
                paramter = p.getText()
                model.paramters.append(paramter)
                print("paramter %s" % (paramter))
        pass


    # Exit a parse tree produced by ChameleonParser#request.
    def exitRequest(self, ctx):
        request = self.topModel()
        generator = None
        if Config.LUANGUAGE_TYPE == LanguageType.Objective_C:
            requestTemplatePath = Config.APP_BIN_PATH+"/../resources/template/oc/request"
            generator = OCRequestGenerator(request, Config.OUTPUT_DIR, None, requestTemplatePath)
            if request.customBuild():
                customG = OCRequestCustomGenerator(request, Config.OUTPUT_DIR, None,Config.APP_BIN_PATH+"/../resources/template/oc/request-custom")
                customG.output(False)
        elif Config.LUANGUAGE_TYPE == LanguageType.Android:
            generator = AndroidRequestGenerator(request, Config.OUTPUT_DIR,None)
        generator.output(True)
        pass

    def enterService(self, ctx):
        name = ctx.ID().getText()
        request = OCServiceModel(name)
        self.models.append(request)

        data = ctx.request_paramters()
        if data == None or len(data) == 0:
            print("NULL paramters")
            return
        print("%s" % (data))
        data = data[0]
        data = data.ID()
        if len(data)>0:
            model = request
            if not isinstance(model, OCRequestModel):
                return
            for p in data:
                paramter = p.getText()
                model.paramters.append(paramter)
                print("paramter %s" % (paramter))
        pass

    def exitService(self, ctx):
        print("service %s" % (ctx.ID().getText()))
        service = self.topModel()

        pass
    def enterComment(self, ctx):
        model = self.topModel().cacheComment(ctx.getText())
        print "*******"
        print "发现注释"
        print ctx.getText()
        print "******"
        pass
        pass
    def generateService(self, service):
        generator = None
        if Config.LUANGUAGE_TYPE == LanguageType.Objective_C:
            requestTemplatePath = Config.APP_BIN_PATH+"/../resources/template/oc/service"
            generator = OCServiceGenerator(service, Config.OUTPUT_DIR, None, requestTemplatePath)
            customServiceTemplatePath = Config.APP_BIN_PATH+"/../resources/template/oc/service-custom"
            customGenerator = OCServiceCustomGenerator(service, Config.OUTPUT_DIR, None, customServiceTemplatePath)
            customGenerator.output(False)

        elif Config.LUANGUAGE_TYPE == LanguageType.Android:
            generator = AndroidRequestGenerator(service, Config.OUTPUT_DIR,None)
        generator.output(True)
        pass
    def exitProg(self,ctx):
        services = filter(lambda x: isinstance(x,OCServiceModel) , self.models)
        requests = filter(lambda x: isinstance(x,OCRequestModel) and (not isinstance(x, OCServiceModel)) , self.models)
        if len(services) > 0:
            for s in services:
                s.subrequests = requests
                self.generateService(s)
        pass
