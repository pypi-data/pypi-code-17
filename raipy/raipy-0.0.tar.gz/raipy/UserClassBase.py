# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 06:30:12 2017

@author: Yuki
"""

def copyTemplate(path):
    import shutil
    import raipy
    rootPath=raipy.__file__.rsplit('\\',1)[0] #the folder contains __init__.py
    shutil.copyfile(rootPath+"\\template.py", path)

class ControlBase():
    bools=[]
    sliders=[]
    dials=[]
    floats=[]
    
    @classmethod
    def get_bools(cls):
        return cls.bools
    
    @classmethod
    def get_sliders(cls):
        return cls.sliders
    
    @classmethod
    def get_dials(cls):
        return cls.dials
    
    @classmethod
    def get_floats(cls):
        return cls.floats

class InstrumentBase():
    insts=[]

    @classmethod
    def getInsts(cls):
        return cls.insts

class OutputBase():
    graph_settings=[]
    graph_outputs=[]
    lcd_outputs=[]
    file_outputs=[]
    
    @classmethod
    def get_graph_units(cls):
        return [output[1] for output in cls.graph_outputs]

    @classmethod
    def get_graph_labels(cls):
        #labelsの書式は[['label_0','unit_0'],['label_1','unit_1']]
        return [output[0] for output in cls.graph_outputs]
    
    @classmethod
    def get_lcd_units(cls):
        return [output[1] for output in cls.lcd_outputs]

    @classmethod
    def get_lcd_labels(cls):
        #labelsの書式は[['label_0','unit_0'],['label_1','unit_1']]
        return [output[0] for output in cls.lcd_outputs]
    
    @classmethod
    def get_file_units(cls):
        return [output[1] for output in cls.file_outputs]

    @classmethod
    def get_file_labels(cls):
        #labelsの書式は[['label_0','unit_0'],['label_1','unit_1']]
        return [output[0] for output in cls.file_outputs]
    
    @classmethod
    def get_graph_settings(cls):
        #graph_settingsの書式は[[x_label,[y_label1,y_label2],[color1,color2]],[２個めのsetting]]
        return cls.graph_settings
    


