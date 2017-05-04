# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:11:01 2017

@author: Yuki
"""
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignal

import raipy.UserClassBase as UserClassBase

class MyPathBox(QWidget):
    '''ファイルパスを表示するためのクラス　読み取りのみ可'''
    graphLabelChangeSig=pyqtSignal(list)
    graphUnitChangeSig=pyqtSignal(list)
    graphSettingSig=pyqtSignal(list)
    lcdLabelChangeSig=pyqtSignal(list)
    lcdUnitChangeSig=pyqtSignal(list)
    instChangeSig=pyqtSignal(list)
    boolChangeSig=pyqtSignal(list)
    sliderChangeSig=pyqtSignal(list)
    dialChangeSig=pyqtSignal(list)
    floatChangeSig=pyqtSignal(list)
    def __init__(self):
        super().__init__()
        f_button=QPushButton('open')
        f_button.pressed.connect(self.showDialog)
        re_button=QPushButton('reload')
        re_button.pressed.connect(self.rePressed)
        temp_button=QPushButton('template')
        temp_button.pressed.connect(self.tempPressed)
        buttons=QHBoxLayout()
        buttons.addWidget(f_button)
        buttons.addWidget(re_button)
        buttons.addWidget(temp_button)
        buttons.addStretch(1)
        
        path_label=QLabel('program file:')
        self.pathEdit = QLineEdit()
        path_layout=QHBoxLayout()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.pathEdit)
        self.pathEdit.setReadOnly(True)
        
        self.dataFile=None
        self.columns=[]
        data_label=QLabel('data file:')
        self.dataEdit=QLineEdit()
        data_layout=QHBoxLayout()
        data_layout.addWidget(data_label)
        data_layout.addWidget(self.dataEdit)
        self.dataEdit.setReadOnly(True)
        
        pathGrid = QVBoxLayout()
        pathGrid.addLayout(buttons)
        pathGrid.addLayout(path_layout)
        pathGrid.addLayout(data_layout)
        
        self.setLayout(pathGrid)
        
        self.program=None    #参照
        self.module=None    #文字列
        
    def showDialog(self):
        #ファイルが指定される度にimportが実際に実行されるようにし、pathが溜まらないようにする
        path = QFileDialog.getOpenFileName(self, 'select a program')
        self.importFile(path)
        
    def rePressed(self):
        self.importFile(self.pathEdit.text())
        
    def tempPressed(self):
        path = QFileDialog.getSaveFileName(self, 'create a template','template.py')
        if path:
            UserClassBase.copyTemplate(path)
            self.importFile(path)
            
    def showDataDialog(self):
        #ファイルを作れたらTrueを返す
        path = QFileDialog.getSaveFileName(self, 'create a file to write data')
        if not path=='':
            self.dataEdit.setText(path)
            self.data_file_init(path,self.get_file_columns(),self.get_file_columns_with_unit())
            return True
        else:
            return False
            
    def importFile(self,path):
        if self.checkFile(path):    #.pyファイル以外（キャンセルも含む)は何もしない
            pre_path=self.pathEdit.text()
            if not pre_path=='':    #''でないということはimportが行われた後ということなのでこれを除去する
                folder=pre_path.rsplit('/',1)[0]
                if sys.path[0]==folder:
                    sys.path.pop(0)
                    sys.modules.pop(self.module)
            
            #programをモジュールとして読み込んでグラフの軸の選択肢をMyQComboBoxに通知    
            self.pathEdit.setText(path)
            folder=path.rsplit('/',1)[0]
            fname=path.rsplit('/',1)[1]
            self.module=fname.split('.')[0]
            sys.path.insert(0,folder)   #先頭に追加することでimport時に一番最初に検索される
            self.program= __import__(self.module)
            self.graphLabelChangeSig.emit(self.get_graph_labels())
            self.graphUnitChangeSig.emit(self.get_graph_units())
            self.lcdLabelChangeSig.emit(self.get_lcd_labels())
            self.lcdUnitChangeSig.emit(self.get_lcd_units())
            self.instChangeSig.emit(self.getInsts())
            self.sliderChangeSig.emit(self.getSliders())
            self.boolChangeSig.emit(self.getBools())
            self.dialChangeSig.emit(self.getDials())
            self.floatChangeSig.emit(self.getFloats())
            self.graphSettingSig.emit(self.get_graph_settings())
        else:
            print('拡張子が.pyで規格を満たしているファイルを指定してください templateボタンで例を出力できます')
            
    def checkFile(self,path):
        try:
            fname=path.rsplit('/',1)[1]
            extension=fname.rsplit('.')[1]
            if extension=='py':
                return True
            else:
                return False
        except:
            return False
        
    def data_file_close(self):
        self.dataFile.close()
        
    def write_data(self,mydict):
        for column in self.columns:
            self.dataFile.write(str(mydict[column])+'\t')
        self.dataFile.write('\n')
        
    def data_file_init(self,file,columns,columns_u):
        #データファイルの初期化
        self.dataFile=open(file,'a+')
        self.columns=columns
        for column in columns_u:
            self.dataFile.write(column+'\t')
        self.dataFile.write('\n')
        
    def get_graph_settings(self):
        #グラフノセッティング
        temp=self.program.Output.get_graph_settings()
        return temp
#        try:
#            return self.program.Output.get_graph_settings()
#        except:
#            raise AttributeError('templateファイルを参照してUserClassBase.OutputBaseを継承したクラスを定義してください')
        
    def get_graph_labels(self):
        #グラフのラベル
        try:
            return self.program.Output.get_graph_labels()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.OutputBaseを継承したクラスを定義してください')

    def get_graph_units(self):
        #グラフのラベルの単位
        try:
            return self.program.Output.get_graph_units()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.OutputBaseを継承したクラスを定義してください')
            
    def get_lcd_labels(self):
        #液晶用のラベル　単位付き
        try:
            return self.program.Output.get_lcd_labels()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.OutputBaseを継承したクラスを定義してください')

    def get_lcd_units(self):
        #液晶用のラベル　単位無し
        try:
            return self.program.Output.get_lcd_units()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.OutputBaseを継承したクラスを定義してください')
            
    def get_file_columns(self):
        #ファイルのcolumn名　単位付き
        try:
            return self.program.Output.get_file_labels()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.OutputBaseを継承したクラスを定義してください')
            
    def get_file_columns_with_unit(self):
        #ファイルのcolumn名　単位付き
        try:
            strings=[label+'('+unit+')' for label,unit in zip(self.program.Output.get_file_labels(),self.program.Output.get_file_units())]
            return strings
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.OutputBaseを継承したクラスを定義してください')

    def getInsts(self):
        #測定器のリストを返す
        try:
            return self.program.Instrument.getInsts()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.InstrumentBaseを継承したクラスを定義してください')
            
    def getBools(self):
        try:
            return self.program.Control.get_bools()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.controlBaseを継承したクラスを定義してください')
            
    def getSliders(self):
        try:
            return self.program.Control.get_sliders()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.controlBaseを継承したクラスを定義してください')
    
    def getDials(self):
        try:
            return self.program.Control.get_dials()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.controlBaseを継承したクラスを定義してください')
    
    def getFloats(self):
        try:
            return self.program.Control.get_floats()
        except:
            raise AttributeError('templateファイルを参照してUserClassBase.controlBaseを継承したクラスを定義してください')
            
if __name__=='__main__':
    app = QApplication(sys.argv)
    f=MyPathBox()
    f.data_file_init('C:\\Users\\Yuki\\Desktop\\datafile',['Temperature','Voltage'])
    f.write_data({'Temperature':300,'Voltage':0.0001})
    f.data_file_close()
    f.show()
    sys.exit(app.exec_())