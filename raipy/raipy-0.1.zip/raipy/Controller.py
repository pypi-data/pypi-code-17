# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:52:16 2017

@author: Yuki
"""
from raipy.Constant import *

from PyQt5.QtWidgets import QWidget,QLabel,QSlider,QDial,QLineEdit,QPushButton,QScrollArea,QHBoxLayout,QVBoxLayout,QSizePolicy
from PyQt5.QtCore import Qt,pyqtSignal
from abc import ABCMeta, abstractmethod

class MyController(QWidget):
    '''ラベル付きのコントローラーの基底クラス'''
    valueChanged=pyqtSignal(dict)
    def __init__(self,name,init):
        super().__init__()
        self.label=QLabel(name)
        self.current=QLabel()
        self.label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.controller = self.getController()  # 継承クラスの実装による
        self.init=init #初期値は記憶しておく
        
        hbox=QHBoxLayout()
        vbox=QVBoxLayout()
        hbox.addWidget(self.label)
        hbox.addWidget(self.current)
        vbox.addLayout(hbox)
        vbox.addWidget(self.controller)
        
        self.setLayout(vbox)
     
    @classmethod
    @abstractmethod    
    def getController(cls):
        '''継承クラスでSliderやDialを返す'''
        raise NotImplementedError('このメソッド抽象メソッドです。子クラスで追加するcontrollerを返すメソッドを実装してください')
        
    def emit(self,value):
        self.valueChanged.emit({self.label.text():value})
        
    @abstractmethod    
    def getInit(self):
        raise NotImplementedError('このメソッド抽象メソッドです。子クラスでcontrollerの現在値を返すメソッドを実装してください')
        
    def lock(self):
        self.controller.setEnabled(False)
        
    def unlock(self):
        self.controller.setEnabled(True)
        
class MySlider(MyController):
    def __init__(self,name,minmum,maximum,init):
        super().__init__(name,init)
        self.controller.valueChanged.connect(self.current.setNum)
        self.controller.valueChanged.connect(self.emit)
        self.controller.setRange(minmum, maximum)  # スライダの範囲
        self.controller.setTickPosition(QSlider.TicksBothSides)
        self.controller.setValue(self.init)  # 初期値セット
        self.current.setNum(self.init)
        
    def getController(cls):
        return QSlider(Qt.Horizontal)
    
    def getInit(self):
        return self.controller.value()
        
class MyDial(MyController):
    def __init__(self,name,minmum,maximum,init):
        super().__init__(name,init)
        self.controller.valueChanged.connect(self.current.setNum)
        self.controller.valueChanged.connect(self.emit)
        self.controller.setRange(minmum, maximum)  # スライダの範囲
        self.controller.setNotchesVisible(True)
        self.controller.setValue(self.init)  # 初期値セット
        self.current.setNum(self.init)
        
    def getController(cls):
        return QDial()
    
    def getInit(self):
        return self.controller.value()
        
class MyFloat(MyController):
    def __init__(self,name,init):
        super().__init__(name,init)
        self.value=init
        self.controller.returnPressed.connect(self.setValue)
        self.controller.setText(str(init))
        self.current.setText(str(init))
        
    def getController(cls):
        return QLineEdit()
        
    def setValue(self):
        try:
            text=self.controller.text() #要求された文字列が数値に変換できるかチェックしてできなければ変更拒否
            self.value=float(text)
            self.current.setText(str(self.value))
            self.emit(self.value)
        except:
            pass
        
    def getInit(self):
        return float(self.current.text())
        
class MyBool(MyController):
    def __init__(self,name,init):
        super().__init__(name,init)
        self.value=init
        self.controller.pressed.connect(self.pressed)
        self.setButtonColor(self.value)
        self.current.setText(str(self.value))
        
    def getController(cls):
        return QPushButton('push')
        
    def pressed(self):
        self.value=not self.value
        self.current.setText(str(self.value))
        self.setButtonColor(self.value)
        self.emit(self.value)
        
    def setButtonColor(self,value):
        if value:
            self.controller.setStyleSheet("background-color: rgb(71,234,126)")
        else:
            self.controller.setStyleSheet(None)
            
    def getInit(self):
        return self.value
    
class MyContainer(QWidget):
    #refで指定されるオブジェクトのリストを表示するクラス
    valueChanged=pyqtSignal(dict)
    def __init__(self,ref_getparams,ref_signal,gene,state_ref):
        super().__init__()
        self.vbox=QVBoxLayout()
        self.setLayout(self.vbox)
        self.children=[]
        
        #scrollAreaの設定childはcvboxに追加していく
        scroll=QScrollArea()
        scroll.setWidgetResizable(True)
        temp=QWidget()
        self.cvbox=QVBoxLayout()
        temp.setLayout(self.cvbox)
        scroll.setWidget(temp)
        self.vbox.addWidget(scroll)
        
        
        self.gene=gene #childの生成関数
        try:
            self.update(ref.getparams)
        except:
            self.update([])
        ref_signal.connect(self.update)
        
        self.state=state_ref.state
        state_ref.stateSignal.connect(self.setState)

    def update(self,params):
        #childrenをセット
        self.reset()
        for param in params:
            child=self.gene(*tuple(param))
            child.valueChanged.connect(self.emit)
#            child.lock()
            self.cvbox.addWidget(child)
            self.children.append(child)
        
    def reset(self):
        '''全て消去'''
        while self.children:
            child=self.children.pop()
            child.valueChanged.disconnect()
            child.setParent(None)
            
    def getInits(self):
        inits={}
        for child in self.children:
            inits[child.label.text()]=child.getInit()
        return inits
            
    def emit(self,mydict):
        #childから送られるsignalは{label:value}なのでそれをそのまま放出
        self.valueChanged.emit(mydict)
        
    def lock(self):
        for child in self.children:
            child.lock()
            
    def unlock(self):
        for child in self.children:
            child.unlock()
        
    def setState(self,state):
        '''状態に応じて付け加えるbarをlockかunlockか切り替える 遷移時には一括で切り替える'''
        self.state=state
        if self.state==RUNNING:
            self.unlock()
#        else:
#            self.lock()