# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:11:01 2017

@author: Yuki
"""
from raipy.Constant import *

from PyQt5.QtCore import QSize,pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog,QComboBox,QSizePolicy,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QFrame,QRadioButton,QGroupBox,QLabel,QScrollArea
from abc import ABCMeta, abstractmethod
from multiprocessing import Process, Queue

from raipy.MyPyqtGraph import *

class MyQComboBox(QComboBox):
    #ref_methodで取得でき、変更があるとref_signalがemitされるリストを表示するクラス
    def __init__(self,ref_method,ref_signal):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        try:
            try:    #まだ値を返せないのはファイルが指定されていない時
                for string in ref_method():
                    self.addItem(string)
            except:
                pass
            ref_signal.connect(self.update)
        except:
            raise Exception('<class MyQComboBox>:getComboListとlistChangeSigを実装したクラスを引数にして初期化してください')
            
    def sizeHint(self):
        return QSize(200,30)
            
    def update(self,newlist):
        for i in range(self.count()):
            self.removeItem(0)
        for string in newlist:
            self.addItem(string)
            
    def setCurrentText(self,text):
        index=self.findText(text)
        self.setCurrentIndex(index)
            
class MyCombo(QWidget):
    '''MyQComboBoxとカラー選択をセットにしたクラス'''
    def __init__(self,ref_method,ref_signal,color=None):
        super().__init__()
        main_layout=QVBoxLayout()
        dialog_layout=QHBoxLayout()
        
        self.combo=MyQComboBox(ref_method,ref_signal)
        
        btn=QPushButton('color')
        btn.pressed.connect(self.showDialog)
        self.frm=QFrame()
        self.frm.resize(200,200)
        if color==None:
            self.col=QColor(255,255,255) #初期色のデフォルトは白
        elif color.__class__==QColor:
            self.col=color
        else:
            raise TypeError('color must be QColor ojbect')
        self.frm.setStyleSheet('QWidget {background-color:'+self.col.name()+'}')
        
        dialog_layout.addWidget(btn)
        dialog_layout.addWidget(self.frm)
        
        main_layout.addWidget(self.combo)
        main_layout.addLayout(dialog_layout)
        
        self.setLayout(main_layout)
        
    def showDialog(self):
        col = QColorDialog.getColor()

        # 選択された色をメインウィンドウへ表示
        if col.isValid():
            self.frm.setStyleSheet('QWidget {background-color:'+col.name()+'}')
            self.col=col
            
    def get_label(self):
        return self.combo.currentText()
        
    def get_color(self):
        return self.col.toRgb()
    
    def setChoice(self,y):
        #y=[label,color]を想定
        self.combo.setCurrentText(y[0])
        self.frm.setStyleSheet('QWidget {background-color:'+y[1].name()+'}')
        self.col=y[1]

class MyBar(QWidget):
    def __init__(self):
        super().__init__()
        self.radio=QRadioButton()
        self.radio.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.hbox=QHBoxLayout()
        self.hbox.addWidget(self.radio)
        self.setLayout(self.hbox)
        
    def isChecked(self):
        return self.radio.isChecked()

class MyGraphBar(MyBar):
    #x軸ラベル、y軸ラベルのリスト、色のリストをemit
    showSignal=pyqtSignal(str,list,list)
    def __init__(self,ref_method,ref_signal,name='graph'):
        super().__init__()
        group=QGroupBox(name)
        group_layout=QVBoxLayout()
        button_layout=QHBoxLayout()
        combo_layout=QHBoxLayout()
        
        self.xcombo=MyQComboBox(ref_method,ref_signal)
        vs=QLabel('vs')
        self.ycombos=MyContainor(ref_method,ref_signal)
        combo_layout.addWidget(self.xcombo)
        combo_layout.addWidget(vs)
        combo_layout.addWidget(self.ycombos)
        
        self.button=QPushButton('show')
        self.button.pressed.connect(self.emitSignal)
        button_layout.addWidget(self.button)
        button_layout.addStretch(1)
        
        group_layout.addLayout(button_layout)
        group_layout.addLayout(combo_layout)
        group.setLayout(group_layout)
        
        self.hbox.addWidget(group)
            
    def emitSignal(self):
        xlabel=self.xcombo.currentText()
        ys=self.ycombos.get_children()
        ylabels=[]
        for y in ys:
            ylabels.append(y.get_label())
        colors=[]
        for y in ys:
            colors.append(y.get_color())
        self.showSignal.emit(xlabel,ylabels,colors)
        
    def lock(self):
        self.button.setEnabled(False)
        
    def unlock(self):
        self.button.setEnabled(True)
        
    def setChoice(self,x,ys):
        self.xcombo.setCurrentText(x)
        self.ycombos.setChoice(ys)      

class MyContainor(QGroupBox):
    '''+,-ボタンでWidgetの追加、削除をするコンテナ'''
    def __init__(self,*args,name='Ys',gene=MyCombo,direction='Horizontal'):
        super().__init__(name)
        if issubclass(gene,QWidget):
            self.gene=gene #追加するオブジェクトのコンストラクタ
            self.args=args #positional引数をそのままコンストラクタに渡す
        else:
            raise TypeError('MyContainor can only contain QWidget and its subclass')
        addButton=QPushButton('+')
        delButton=QPushButton('-')
        addButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        delButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        addButton.pressed.connect(self.add)
        delButton.pressed.connect(self.delete)
        bbox=QHBoxLayout()
        bbox.addWidget(addButton)
        bbox.addWidget(delButton)
        bbox.addStretch(1)
        
        box=QVBoxLayout()
        box.addLayout(bbox)
        
        combos=QWidget() #拡大用のWidget これにlayoutを乗せる
        combos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout=QHBoxLayout()
        stretch=QHBoxLayout()
        stretch.addStretch(1)
        if direction=='Horizontal':
            self.combo_box=QHBoxLayout()
        else:
            self.combo_box=QVBoxLayout()
        layout.addLayout(self.combo_box)
        layout.addLayout(stretch)
        combos.setLayout(layout)
        box.addWidget(combos)
        
        self.setLayout(box)
        self.children=[]

    def add(self):
        child=self.gene(*self.args)
        self.combo_box.addWidget(child)
        self.children.append(child)
        return child
        
    def delete(self):
        if len(self.children)>0:
            child=self.children.pop()
            child.setParent(None)
        
    def get_children(self):
        return tuple(self.children)
    
    def setChoice(self,ys):
        #一旦全消去
        while self.children:
            self.delete()
        for y in ys:
            child=self.add()
            child.setChoice(y)
            
        
        
class MyList(QGroupBox):
    '''+,-で追加と削除が可能なリストの抽象クラス'''
    __metaclass__=ABCMeta
    def __init__(self,name):
        super().__init__(name)
        self.addButton=QPushButton('+')
        self.delButton=QPushButton('-')
        self.addButton.pressed.connect(self.add)
        self.delButton.pressed.connect(self.delete)
        hbox=QHBoxLayout()
        hbox.addWidget(self.addButton)
        hbox.addWidget(self.delButton)
        hbox.addStretch(1)
        self.vbox=QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.setLayout(self.vbox)
        self.barList=[]

    @classmethod
    @abstractmethod
    def add(self):
        '''isCheckedメソッドを実装しているQWidgetを追加する'''
        raise NotImplementedError()
        
    @classmethod
    @abstractmethod
    def delete(self):
        '''繋いだシグナルは外す'''
        raise NotImplementedError()       
        
class MyGraphManager(MyList):
    '''描画するグラフを保持する　+,-で追加と削除が可能'''
    def __init__(self,string,label_method,unit_method,label_signal,unit_signal,setting_signal,state_ref):
        super().__init__(string)
        self.data={}
        self.graphs=[]   #{'process':process,'que':que}のリストを保持する
        
        #scrollAreaの設定 barはcvboxに追加していく
        scroll=QScrollArea()
        scroll.setWidgetResizable(True)
#        scroll.setFixedHeight(300)
        temp=QWidget()
        self.cvbox=QVBoxLayout()
        temp.setLayout(self.cvbox)
        scroll.setWidget(temp)
        self.vbox.addWidget(scroll)
        
        #状態とcomvoboxのリストの参照先を決定
        self.label_method=label_method
        self.label_signal=label_signal
        try:
            self.labels=label_method()
            self.units=unit_method()
        except:
            self.labels=[]
            self.units=[]
        label_signal.connect(self.update_labels)
        unit_signal.connect(self.update_units)
        setting_signal.connect(self.set_default)
        
        self.state=state_ref.state
        state_ref.stateSignal.connect(self.setState)
        
    def add(self):
        gbar=MyGraphBar(self.label_method,self.label_signal)
#        if not self.state==RUNNING:
#            gbar.lock()
        gbar.showSignal.connect(self.graphGene)
        self.cvbox.addWidget(gbar)
        self.barList.append(gbar)   #親クラスのメンバ
        return gbar
        
    def delete(self):
        delList=[x for x in self.barList if x.isChecked()==True]
        newList=[x for x in self.barList if x.isChecked()==False]
        for x in delList:
            x.setParent(None)
            x.showSignal.disconnect(self.graphGene)
        self.barList=newList
        
    def set_default(self,settings):
        #全てクリア
        for bar in self.barList:
            bar.setParent(None)
            bar.showSignal.disconnect(self.graphGene)
        self.barList=[]
        
        for setting in settings:
            #ユーザ定義のlistからsetChoiceの引数への変換 ユーザ定義の書式はUserClassBaseに記述
            xlabel=setting[0]
            ylabels=setting[1]
            colors=setting[2]
            ys=[[y,c] for (y,c) in zip(ylabels,colors)]
            bar=self.add()
            bar.setChoice(xlabel,ys)
        
            
    def initData(self):
        '''dataの格納場所を確保する 例えばTime/secの系列はself.data['Time/sec']にappendしていく 前回のが残っているかもしれなのでフラッシュ'''
        self.data={}
        self.graphs=[]
        for string in self.labels:
            self.data[string]=[]
        print('-----------display values---------------\n')
        print(self.labels)
            
    def updateData(self,mydict):
        for key in mydict:
            self.data[key].append(mydict[key])
        for graph in self.graphs:
            if graph['process'].is_alive():
                graph['que'].put(mydict)
            else:   #閉じられたグラフのqueは空であることを保証する queに値が残っているとinitDataでself.graphs=[]時にパイプエラーが起きる
                self.empty_que(graph['que'])
            
    def update_labels(self,labels):
        self.labels=labels
        
    def update_units(self,units):
        self.units=units
            
    def graphGene(self,xlabel,ylabels,colors):
        if self.check_input(ylabels):
            index=self.barList.index(self.sender())
            que=Queue()
            x_unit=self.units[self.labels.index(xlabel)]
            y_unit=self.units[self.labels.index(ylabels[0])]
            ydatas=[self.data[ylabel] for ylabel in ylabels]
            p=Process(target=graphDraw,args=(xlabel,x_unit,ylabels,y_unit,colors,self.data[xlabel],ydatas,que))
            self.graphs.append({'process':p,'que':que})
            p.start()
        else:
            print('ラベルに重複が無いことと、それらの単位が同じであるかチェックしてください')
        
    def check_input(self,ylabels):
        #同じラベルがあるとダメ
        ylabels_set=set(ylabels)
        if len(ylabels_set)<len(ylabels):
            return False
        else:
            #単位が違うとダメ
            ylabels_unit=[unit for label,unit in zip(self.labels,self.units) if label in ylabels]
            if len(set(ylabels_unit))==1:
                return True
            else:
                return False
        
    def lock(self):
        for x in self.barList:
            x.lock()
            
    def unlock(self):
        for x in self.barList:
            x.unlock()
            
    def setState(self,state):
        '''状態に応じて付け加えるbarをlockかunlockか切り替える 遷移時には一括で切り替える'''
        self.state=state
        if self.state==RUNNING:
            self.unlock()
#        else:
#            self.lock()
            
    @classmethod
    def empty_que(cls,que):
        while True:
            if que.empty():
                break
            que.get()