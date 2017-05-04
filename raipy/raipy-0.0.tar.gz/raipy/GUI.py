# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:52:15 2017

@author: Yuki
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignal

from raipy.Constant import *
from raipy.Controller import *
from raipy.FileManager import *
from raipy.GraphManager import *
from raipy.LCD_Display import *
from raipy.MyPyqtGraph import *
from raipy.Time import *
from raipy.Help import helpText

class MyToolBar(QToolBar):
    '''自作Toolbar 状態を持ちその状態によって押せるボタンが変化する その状態としてはQMainWindowの状態を参照する QMainWindowのstateSignalと繋ぐことで状態をupdate'''
    def __init__(self,ref):
        super().__init__()
        self.exeAction=QAction('Run', self)
        self.stopAction = QAction('Stop', self)
        self.questionAction = QAction('Help', self)
        self.addAction(self.exeAction)
        self.addAction(self.stopAction)
        self.addAction(self.questionAction)
        
        self.setState(ref.state)
        ref.stateSignal.connect(self.setState)
        
    def setState(self,end):
        '''状態の遷移はこの関数を通して行われる'''
        if end==INITIAL:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(False)
        elif end==READY:
            self.exeAction.setEnabled(True)
            self.stopAction.setEnabled(False)
        elif end==NOTFOUND:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(False)
        elif end==RUNNING:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            
class GUIWindow(QMainWindow):
    stateSignal=pyqtSignal(int)
    def __init__(self): 
        super().__init__()
        self.state=INITIAL
        self.setWindowIcon(QIcon('.\\icon\\python_logo.png'))
        self.initUI()
        self.setState(INITIAL)
        self.params={} #programThreadの生成時に渡してcontrollerによる制御を可能にする
        
    def initUI(self):               
        #Toolbarを付ける
        toolbar=MyToolBar(self)
        toolbar.exeAction.triggered.connect(self.exePressed)
        toolbar.stopAction.triggered.connect(self.stopPressed)
        toolbar.questionAction.triggered.connect(self.questionPressed)
        self.addToolBar(toolbar)
        
        
        #tab1
        self.pathbox=MyPathBox()
        self.pathbox.instChangeSig.connect(self.fileAppointed)
        self.gm=MyGraphManager('Graphs',self.pathbox.get_graph_labels,self.pathbox.get_graph_units,\
                               self.pathbox.graphLabelChangeSig,self.pathbox.graphUnitChangeSig,self.pathbox.graphSettingSig,self)
        vbox=QVBoxLayout()
        vbox.addWidget(self.pathbox)
        vbox.addWidget(self.gm)
        setTab=QWidget()
        setTab.setLayout(vbox)
        
        #tab2
        self.lcdContainer=MyLCDContainer(self.pathbox.get_lcd_labels,self.pathbox.get_lcd_units,\
                                         self.pathbox.lcdLabelChangeSig,self.pathbox.lcdUnitChangeSig,self)
        self.time=MyTimeBox()
        #サイズ調整
        sizePolicyTime=self.time.sizePolicy()
        sizePolicyLcd=self.lcdContainer.sizePolicy()
        sizePolicyTime.setHorizontalStretch(1)
        sizePolicyLcd.setHorizontalStretch(1)
        self.time.setSizePolicy(sizePolicyTime)
        self.lcdContainer.setSizePolicy(sizePolicyLcd)
        
        hbox=QHBoxLayout()
        hbox.addWidget(self.lcdContainer)
        hbox.addWidget(self.time)
        displayTab=QWidget()
        displayTab.setLayout(hbox)
        
        #tab3
        self.sContainer=MyContainer(self.pathbox.getSliders,self.pathbox.sliderChangeSig,MySlider,self)
        self.bContainer=MyContainer(self.pathbox.getBools,self.pathbox.boolChangeSig,MyBool,self)
        self.dContainer=MyContainer(self.pathbox.getDials,self.pathbox.dialChangeSig,MyDial,self)
        self.fContainer=MyContainer(self.pathbox.getFloats,self.pathbox.floatChangeSig,MyFloat,self)
        self.sContainer.valueChanged.connect(self.updateParam)
        self.bContainer.valueChanged.connect(self.updateParam)
        self.dContainer.valueChanged.connect(self.updateParam)
        self.fContainer.valueChanged.connect(self.updateParam)
        hbox2=QHBoxLayout()
        hbox2.addWidget(self.sContainer)
        hbox2.addWidget(self.bContainer)
        hbox2.addWidget(self.dContainer)
        hbox2.addWidget(self.fContainer)
        controlTab=QWidget()
        controlTab.setLayout(hbox2)
        
        #tabをまとめる
        self.qTab=QTabWidget()
        self.qTab.setStyleSheet('QTabWidget::tab-bar{alignment: center;}')  #ツールバーのボタンとの押し間違えを防ぐために中央に配置
        self.qTab.addTab(setTab,'setting')
        self.qTab.addTab(displayTab,'display')
        self.qTab.addTab(controlTab,'control')
        self.setCentralWidget(self.qTab)
        
        #status barを付ける
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        
        #windowを描画
        self.setGeometry(10, 60, 960,900)
        self.setWindowTitle('汎用Interface')    
        
        self.show()
        
    def exePressed(self):
        if self.state==READY:
            if self.pathbox.showDataDialog():
                self.gm.initData()
                self.initParams(self.sContainer.getInits(),self.bContainer.getInits(),self.dContainer.getInits(),self.fContainer.getInits())
                self.thread=self.pathbox.program.programThread(self.params)
                self.thread.lcdSignal.connect(self.lcdContainer.update_data)
                self.thread.finished.connect(self.program_exit)  #stopボタンが押されないまま全ての処理が終わった場合のため
                self.thread.graphSignal.connect(self.gm.updateData)
                self.thread.fileSignal.connect(self.pathbox.write_data)
                self.thread.start()
                self.time.startTimer()
                self.setState(RUNNING)
                self.qTab.setCurrentIndex(1)
            
    def stopPressed(self):
        if self.state==RUNNING:
            self.thread.terminate() #stopでの停止と全部の処理の終了での停止をまとめて処理するため ここでは状態を遷移しない
        
    def questionPressed(self):
        try:
            self.text.showNormal()
        except:
            self.text=QTextEdit()
            self.text.setGeometry(500, 45, 800, 900)
            self.text.setWindowTitle('Help')
            self.text.setFont(QFont('TimesNewRoman',12))
            self.text.setHtml(helpText)
            self.text.setReadOnly(True)
            self.text.show()
        
    def initParams(self,*mydicts):
        self.params={}
        for mydict in mydicts:
            for key in mydict:
                self.params[key]=mydict[key]
        print('----------------control parameters---------------------\n')
        print(self.params)
                
    def updateParam(self,mydict):
        for key in mydict:
            self.params[key]=mydict[key]
        
    def fileAppointed(self,newlist):
        #測定器があるかないかを判定
        if self.instSearch(newlist):
            self.setState(READY)
        else:
            self.setState(NOTFOUND)
        
    @classmethod
    def instSearch(cls,mylist):
        #指定された測定器が繋がっているかチェックする
        temp=['GPIB::4','GPIB::7','GPIB::14']
        return temp==mylist
        
    def program_exit(self):
        self.pathbox.data_file_close()
        self.time.stopTimer()
        self.setState(READY)
        
    def setState(self,state):
        '''状態は必ずこの関数を用いて遷移させる'''
        self.state=state
        if self.state==INITIAL:
            self.status_bar.showMessage('choose file')
        elif self.state==READY:
            self.status_bar.showMessage('ready to start the program')
        elif self.state==NOTFOUND:
            self.status_bar.showMessage('instruments not found')
        elif self.state==RUNNING:
            self.status_bar.showMessage('program is running')
        self.stateSignal.emit(self.state)

#メイン　
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=GUIWindow()
    sys.exit(app.exec_())