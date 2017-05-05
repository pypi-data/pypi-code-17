# -*- coding: utf-8 -*-
import PyQt5.QtCore
from PyQt5.QtGui import QColor
import time
import numpy as np
import math
#import raipy.UserClassBase as UserClassBase
import raipy.UserClassBase as UserClassBase
from datetime import datetime

T='Time'
V='Voltage'
I='Current'

V_A='Voltage Amplitude'
I_A='Current Amplitude'
V_N='Voltage Noise'
I_N='Current Noise'

P='Phase'
MODE='Mode'

HALT='Halt'
FLAG='Noise On'

V_B='Voltage Background level'
I_B='Current Background level'
T_I='Time Interval'


#計測機との通信、ファイルへの書き込みを行うスレッド
class programThread(PyQt5.QtCore.QThread):
    graphSignal=PyQt5.QtCore.pyqtSignal(dict)   #グラフは全てのデータの個数が揃っている必要がある
    lcdSignal=PyQt5.QtCore.pyqtSignal(dict) #こちらはそうで無くても良い
    fileSignal=PyQt5.QtCore.pyqtSignal(dict)
    def __init__(self,params):
        super().__init__()
        self.params=params
    def run(self):
        ##############ここに処理を記述##################################################################################
        ### 例：Temperature,Voltageに値1,2を表示したい場合はself.lcdSignal.emit({'Temperature':1,'Voltage':2})とする
        #############################################################################################################
        print('thread started')
        timeOrigin=datetime.now()
        for i in range(1000000):
            time.sleep(self.params[T_I])
            if not self.params[HALT]:
                t=(datetime.now()-timeOrigin).total_seconds()
                vol=self.params[V_A]*np.sin(t)+self.params[V_B]
                vol_n=self.params[V_N]*np.random.rand()
                cur=self.params[I_A]*np.cos(t+math.pi*self.params[P]/180)+self.params[I_B]
                cur_n=self.params[I_N]*np.random.rand()
                if self.params[MODE]==0:
                    if self.params[FLAG]:
                        vol=(vol+vol_n)/t
                        cur=(cur+cur_n)/t
                    else:
                        vol=vol/t
                        cur=cur/t
                elif self.params[MODE]==1:
                    if self.params[FLAG]:
                        vol=vol+vol_n
                        cur=cur+cur_n
                    else:
                        pass
                else:
                    if self.params[FLAG]:
                        vol=(vol+vol_n)*t
                        cur=(cur+cur_n)*t
                    else:
                        vol=vol*t
                        cur=cur*t
                data={T:t,V:vol,I:cur}
                self.lcdSignal.emit(data)
                self.graphSignal.emit(data)
                self.fileSignal.emit(data)
        print('thread finished.created 1 million data series')

class Instrument(UserClassBase.InstrumentBase):
    ################使用する装置のGPIBアドレスを記述################################################
    ### 例:insts=['GPIB::4','GPIB::7','GPIB::14']
    ##########################################################################################
    insts=['GPIB::4','GPIB::7','GPIB::14']

class Output(UserClassBase.OutputBase):
    ################表示したい測定値を単位付きで記述###############################################
    ### 例:outputs=[['Temperature','K'],['Voltage','V']]
    ##########################################################################################
    graph_settings=[[T,[V,I],[QColor(255,255,0),QColor(0,255,255)]],[V,[I],[QColor(255,0,255)]]]
    graph_outputs=[[T,'s'],[V,'V'],[I,'V']]
    lcd_outputs=[[T,'s'],[V,'V'],[I,'V'],['lcd_only','L'],['lcd_only2','LL']]
    file_outputs=[[T,'s'],[V,'V'],[I,'V']]
    
class Control(UserClassBase.ControlBase):
    bools=[[HALT,False],[FLAG,False]]
    sliders=[[V_A,0,100,50],[I_A,0,100,50],[V_N,0,100,5],[I_N,0,100,5]]
    dials=[[P,0,359,0],[MODE,0,2,2]]
    floats=[[V_B,100],[I_B,100],[T_I,0.01]]