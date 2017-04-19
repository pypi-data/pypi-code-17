# coding: UTF-8
import os
from ..utilities.constant import *
#全局配置变量

class Config(object) :
    OUTPUT_DIR = os.getcwd()
    OC_TYPE = 'mantle'
    TEMPLATE = None
    APP_BIN_PATH = os.path.split(os.path.realpath(__file__))[0];
    LUANGUAGE_TYPE = None
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._inst
    @classmethod
    def setupWithArgs(cls,args):
        od = args.outDir
        if od == None:
            cls.OUTPUT_DIR = os.getcwd()
        else:
            cls.OUTPUT_DIR =  os.path.expanduser(od)
            pass
        cls.TEMPLATE = args.template
        #oc output type
        if cls.TEMPLATE == None:
            type = args.outType
            if type == None:
                type = OCOutType.BWModel
            elif type == OCOutType.Mantle:
                type = OCOutType.Mantle
            elif type == OCOutType.BWModel:
                type = OCOutType.BWModel
            elif type == OCOutType.Dic:
                type = OCOutType.Dic
            else:
                print("不支持该类型的输出")
            cls.OC_TYPE = type
        pass

        language = args.language
        print("language %s" % args.language)
        if language == None:
            print("请输入您要生成的语言类型")
            exit(1)
        if language == LanguageType.Objective_C:
            cls.LUANGUAGE_TYPE = language
        elif language == LanguageType.Android:
            cls.LUANGUAGE_TYPE = language
        else:
            print("您输入的语言类型非法，请检查")
            exit(1)
    pass
