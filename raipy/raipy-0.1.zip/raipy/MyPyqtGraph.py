# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 23:53:11 2017

@author: Yuki
"""

from multiprocessing import Process,Queue

from PyQt5.QtWidgets import QApplication
#プロット関係のライブラリ
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

import time

GRAPH_RATE=10  #グラフのアップデート頻度(ms)

class PlotWindow:
    def __init__(self,x_label,x_unit,y_labels,y_unit,colors,x_init,y_inits,que=None):
        #プロット初期設定
        self.win=pg.GraphicsWindow()
        self.win.setWindowTitle('Graph')
        self.plt=self.win.addPlot()
        self.plt.addLegend()
        
        self.x=x_init
        self.x_last=self.x[-1]
        self.xlabel=x_label
        self.x_unit=x_unit

        self.ys=y_inits
        self.ys_last=[y[-1] for y in self.ys]
        self.ylabels=y_labels
        self.ys_unit=y_unit
        
        self.colors=colors
        self.que=que

        fontCss = {'font-family': "Times New Roman, メイリオ", 'font-size': '14pt', "color": 'white'}
        self.plt.getAxis('bottom').setLabel(**fontCss)
        self.plt.getAxis('left').setLabel(**fontCss)
        self.plt.setLabel('bottom',self.xlabel, units=self.x_unit)
        self.plt.setLabel('left', 'Ys', units=self.ys_unit)
        
        self.curves={}
        self.points={}
        for data,ylabel,color in zip(self.ys,self.ylabels,colors):
            self.curves[ylabel]=self.plt.plot(self.x,data,pen=color,name=ylabel)
        for y_last,ylabel,color in zip(self.ys_last,self.ylabels,colors):
            self.points[ylabel]=self.plt.plot([self.x_last],[y_last],symbolBrush='w')
        
        
        #アップデート時間設定
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(GRAPH_RATE)
        
    def update(self):
        mydicts=self.empty_que()
        if len(mydicts)>0:
            xappended=[d[self.xlabel] for d in mydicts]
            self.x=self.x+xappended
            self.x_last=xappended[-1]
            for index,ylabel in enumerate(self.ylabels):
                yappended=[d[ylabel] for d in mydicts]
                self.ys[index]=self.ys[index]+yappended
                self.ys_last[index]=yappended[-1]
                self.curves[ylabel].setData(self.x,self.ys[index])
                #点有りだとsetDataのエラーがでる(おそらくpyqtgraphの問題)ので全て消去してから、再度plot
                self.plt.removeItem(self.points.pop(ylabel))
            for y_last,ylabel,color in zip(self.ys_last,self.ylabels,self.colors):
                self.points[ylabel]=self.plt.plot([self.x_last],[y_last],symbolBrush='w')
        
    def empty_que(self):
        '''キューにたまっているdictionary型を全てpopしてlist形式にして返す'''
        mydicts=[]
        while True:
            if self.que.empty():
                break
            mydicts.append(self.que.get())
        return mydicts
        
def graphDraw(x_label,x_unit,y_labels,y_unit,colors,x_init,y_inits,que):
    app = QApplication(sys.argv)
    graph=PlotWindow(x_label,x_unit,y_labels,y_unit,colors,x_init,y_inits,que)
    sys.exit(app.exec_())

if __name__=='__main__':
    app = QApplication(sys.argv)
    x=np.arange(0,10000,0.1)
    y1=np.random.rand(100000)
    y2=np.random.rand(100000)+1
    g=PlotWindow('x','A',['y1','y2'],'V',[QColor(255,0,0),QColor(0,255,0)],x,[y1,y2],Queue())
    sys.exit(app.exec_())