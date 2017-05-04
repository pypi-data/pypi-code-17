# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:52:15 2017

@author: Yuki
"""
from raipy.Constant import *

from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignal,Qt,QTimer

class MyLCDNumber(QWidget):
    indexChangeSig=pyqtSignal(int)
    def __init__(self,label,unit,color=QColor(255,255,255),digit=12):
        super().__init__()
        #見た目の調整
        #単位はRangeの切り替えで切り替わる
        #sliderによってlcdの更新のスピードを切り替える
        self.label=label
        self.unit=unit
        self.text=QLabel(label+' '+'('+unit+')')    #実際に表示されるテキスト
        self.text.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        
        self.slider=QSlider(Qt.Horizontal)
        self.slider.setRange(10,1000)   #lcd更新のinterval 単位はms
        self.slider.setValue(10)
        self.slider.valueChanged.connect(self.set_timer)
        self.buffer=0   #ここにいったん更新値をためてself.timerの間隔で液晶を更新する
        
        
        self.upButton=QPushButton('▲')
        self.upButton.pressed.connect(self.incre_index)
        self.upButton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.downButton=QPushButton('▼')
        self.downButton.pressed.connect(self.decre_index)
        self.downButton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.lcd=QLCDNumber()
        self.lcd.setMinimumHeight(100)
        self.color=color
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        
        self.lcd.setAutoFillBackground(True)
        palette=self.lcd.palette()
        palette.setColor(palette.WindowText,self.color)
        palette.setColor(palette.Window,QColor(0,0,0))
        self.lcd.setPalette(palette)
        self.lcd.setDigitCount(digit)
        
        hbox=QHBoxLayout()
        hbox.addWidget(self.text)
        hbox.addStretch()
        hbox.addWidget(self.slider)
        hbox.addWidget(self.upButton)
        hbox.addWidget(self.downButton)
        vbox=QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.lcd)
        self.setLayout(vbox)
        
        #Rangeの調整
        self.range=[1e-12,1e-9,1e-6,1e-3,1,1e3,1e6,1e9,1e12]
        self.prephix=['p','n','mu','m','','k','M','G','T']
        self.index=4
        self.indexChangeSig.connect(self.change_prephix)
        
        #アップデート時間設定
        self.timer=QTimer()
        self.timer.timeout.connect(self.update_lcd)
        self.timer.start(10)
        
    def set_timer(self,num):
        self.timer.timeout.disconnect()
        self.timer=QTimer()
        self.timer.timeout.connect(self.update_lcd)
        self.timer.start(num)
    
    def update_lcd(self):
        self.lcd.display(self.buffer)
        
        
    def incre_index(self):
        if not self.index==len(self.range)-1:
            self.index+=1
            self.indexChangeSig.emit(self.index)
            
    def decre_index(self):
        if not self.index==0:
            self.index-=1
            self.indexChangeSig.emit(self.index)
            
    def change_prephix(self,index):
        unit='('+self.prephix[index]+self.unit+')'
        self.text.setText(self.label+' '+unit)
        
    def update_value(self,value):
        #valueのkeyは単位無しなので注意する また必ず自身が更新すべき値が入っているとは限らない
        try:
            raw=value[self.label]
            final=raw/self.range[self.index]
            self.buffer=final
        except:
            pass
        
    def lock(self):
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        
    def unlock(self):
        self.upButton.setEnabled(True)
        self.downButton.setEnabled(True)
        
class MyLCDContainer(QWidget):
    #液晶ディスプレイのコンテナクラス
    updateSignal=pyqtSignal(dict)
    setSignal=pyqtSignal(list,list)
    def __init__(self,label_method,unit_method,label_signal,unit_signal,state_ref):
        super().__init__()
        self.vbox=QVBoxLayout()
        self.setLayout(self.vbox)
        self.lcdList=[]
        
        #scrollAreaの設定barはcvboxに追加していく
        scroll=QScrollArea()
        scroll.setWidgetResizable(True)
        temp=QWidget()
        self.cvbox=QVBoxLayout()
        temp.setLayout(self.cvbox)
        scroll.setWidget(temp)
        self.vbox.addWidget(scroll)
        
        try:
            self.update_lcd(label_method(),unit_method())
        except:
            self.update_lcd([],[])
            
        self.labels=[]
        self.units=[]
        label_signal.connect(self.set_labels)
        unit_signal.connect(self.set_units)
        self.setSignal.connect(self.update_lcd)
        
        self.state=state_ref.state
        state_ref.stateSignal.connect(self.setState)
        
    def set_labels_units(self):
        #labelとunitが揃った時点で更新を行う
        self.setSignal.emit(self.labels,self.units)
        self.labels=[]
        self.units=[]
        
    def set_labels(self,labels):
        self.labels=labels
        if not self.units==[]:
            self.set_labels_units()
        
    def set_units(self,units):
        self.units=units
        if not self.labels==[]:
            self.set_labels_units()

    def update_lcd(self,labels,units):
        '''ラベルを本体と単位に分けてセットする'''
        self.reset()
        for index,(label,unit) in enumerate(zip(labels,units)):
            lcd=MyLCDNumber(label,unit,self.colorMap(index))
#            lcd.lock()
            self.updateSignal.connect(lcd.update_value)
            self.cvbox.addWidget(lcd)
            self.lcdList.append(lcd)
        
    def reset(self):
        '''全て消去'''
        for x in self.lcdList:
            self.updateSignal.disconnect(x.update_value)
            x.setParent(None)
        self.lcdList=[]

    def colorMap(self,index):
        colors=[QColor(248,6,6),QColor(0,255,65),QColor(0,255,255),QColor(255,255,0),QColor(255,0,255)]
        if index>=0 and index<len(colors):
            return colors[index]
        else:
            return QColor(255,255,255)
            
    def update_data(self,mydict):
        self.updateSignal.emit(mydict)
        
    def lock(self):
        for lcd in self.lcdList:
            lcd.lock()
            
    def unlock(self):
        for lcd in self.lcdList:
            lcd.unlock()
        
    def setState(self,state):
        '''状態に応じて付け加えるbarをlockかunlockか切り替える 遷移時には一括で切り替える'''
        self.state=state
        if self.state==RUNNING:
            self.unlock()
#        else:
#            self.lock()