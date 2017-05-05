# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:52:15 2017

@author: Yuki
"""
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal,QTimer
from PyQt5.QtWidgets import QLabel,QLCDNumber,QWidget,QLabel,QHBoxLayout,QVBoxLayout,QSizePolicy


from datetime import datetime

class MyTimeEdit(QLCDNumber):
    '''液晶ライクな数字表示器の抽象クラス'''
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timeOrigin=datetime.now()
        
        # set color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.WindowText,QColor(255,255,255))
        palette.setColor(palette.Background,QColor(0,0,0))
        palette.setColor(palette.Light,QColor(100,100,100))
        palette.setColor(palette.Dark,QColor(50,50,50))
        self.setPalette(palette)
    
    def update_value(self):
        print('Abstract')
    
    def stop_update(self):
        self.timer.stop()
        
    def startTimer(self):
        raise NotImplementedError('サブクラスで実装してください')
 
class TotalSecondsEdit(MyTimeEdit):
    '''タイマー（秒）'''
    def __init__(self):
        super().__init__()
        self.setDigitCount(10)
        
    def update_value(self):
        now=datetime.now()
        self.display(int((now-self.timeOrigin).total_seconds()))
        
    def startTimer(self):
        self.timeOrigin=datetime.now()
        self.timer.start(100)        
        
class MyHoursEdit(MyTimeEdit):
    '''タイマーの時間部分'''
    def __init__(self):
        super().__init__()
        self.setDigitCount(4)
        
    def update_value(self):
        now=datetime.now()
        hour=int((now-self.timeOrigin).total_seconds()/3600)
        self.display(hour)
        
    def startTimer(self):
        self.timeOrigin=datetime.now()
        self.timer.start(1000*60)
    
class MyMinutesEdit(MyTimeEdit):
    '''タイマーの分部分'''
    def __init__(self):
        super().__init__()
        self.setDigitCount(4)
        
    def update_value(self):
        now=datetime.now()
        hour=int((now-self.timeOrigin).total_seconds()/3600)
        rest=(now-self.timeOrigin).total_seconds()-hour*3600
        minute=int(rest/60)
        self.display(minute)
        
    def startTimer(self):
        self.timeOrigin=datetime.now()
        self.timer.start(1000)
            
class MySecondsEdit(MyTimeEdit):
    '''タイマーの秒部分'''
    def __init__(self):
        super().__init__()
        self.setDigitCount(4)
        
    def update_value(self):
        now=datetime.now()
        hour=int((now-self.timeOrigin).total_seconds()/3600)
        rest=(now-self.timeOrigin).total_seconds()-hour*3600
        minute=int(rest/60)
        second=int(rest-minute*60)
        self.display(second)
        
    def startTimer(self):
        self.timeOrigin=datetime.now()
        self.timer.start(100)
        
class MyTimeBox(QWidget):
    '''測定の開始時点からの経過時間を表示するクラス'''
    def __init__(self):
        super().__init__()
        time=QLabel('Time')
        time.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.hoursEdit=MyHoursEdit()
        hours=QLabel('h')
        self.minutesEdit=MyMinutesEdit()
        minutes=QLabel('m')
        self.secondsEdit=MySecondsEdit()
        seconds=QLabel('s')
        hBox=QHBoxLayout()
        hBox.addWidget(self.hoursEdit)
        hBox.addWidget(hours)
        hBox.addWidget(self.minutesEdit)
        hBox.addWidget(minutes)
        hBox.addWidget(self.secondsEdit)
        hBox.addWidget(seconds)
        
        totalSeconds=QLabel('total seconds(s):')
        totalSeconds.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.totalSecondsEdit=TotalSecondsEdit()
        vBox=QVBoxLayout()
        vBox.addWidget(time)
        vBox.addLayout(hBox)
        vBox.addWidget(totalSeconds)
        vBox.addWidget(self.totalSecondsEdit)
        
        self.setLayout(vBox)
        
    def startTimer(self):
        self.hoursEdit.startTimer()
        self.minutesEdit.startTimer()
        self.secondsEdit.startTimer()
        self.totalSecondsEdit.startTimer()
        
    def stopTimer(self):
        self.hoursEdit.stop_update()
        self.minutesEdit.stop_update()
        self.secondsEdit.stop_update()
        self.totalSecondsEdit.stop_update()
