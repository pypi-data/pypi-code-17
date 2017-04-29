# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 03:15:02 2017

@author: Yuki
"""
import sys
import pickle
import inspect
from PyQt5.QtCore import QRect,pyqtSignal,Qt
from PyQt5.QtWidgets import QFileDialog,QWidget,QPushButton,QSizePolicy,QHBoxLayout,QVBoxLayout,\
                            QTreeView,QAbstractItemView,QApplication
from PyQt5.QtGui import QColor,QStandardItem,QStandardItemModel

import JupyterHuck.MyTree as MyTree
from JupyterHuck.MyGraph import MyGraphWindow

NAME=0
TYPE=1

def getRoot():
    path = QFileDialog.getSaveFileName(None, 'chose save file','root.jh')
    if not path[0]=='': #pyqt5ではtapleの一個めにpathが入っている
        try:
            root=pickle.load(open(path[0],'rb')) #unpickleできる場合
            root.setview.setSavePath(path[0])
        except:
            root=MyTreeWidget()
            root.setview.setSavePath(path[0])
        return root

def geneMyTreeWidget(view):
    return MyTreeWidget(view=view)
        
class MyTreeWidget(QWidget):
    def __init__(self,view=None):
        super().__init__()
        if view==None:
            self.setview=MyTreeView()
        else:
            self.setview=view
        self.cur=self.setview.cur
        self.setview.setmodel.mytree.currentSignal.connect(self.setCurrent)
        
        style='''
            background-color:rgb(55,62,75);
            border-color: gray;
            '''
        self.setStyleSheet(style)
        
        button_style='''
                    QPushButton {background-color: white;
                                 border-style: none;
                                 border-radius: 5px;
                                 font: bold 14px;
                                 min-width: 5em;
                                 padding: 6px;
                                 }
                    QPushButton:pressed {background-color: rgb(200,200,200);}
                    '''
        addButton=QPushButton('+')
        delButton=QPushButton('-')
        addButton.setStyleSheet(button_style)
        delButton.setStyleSheet(button_style)
        addButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        delButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        addButton.pressed.connect(self.setview.add)
        delButton.pressed.connect(self.setview.delete)
        bbox=QHBoxLayout()
        bbox.addWidget(addButton)
        bbox.addWidget(delButton)
        bbox.addStretch(1)
        
        self.vbox=QVBoxLayout()
        self.vbox.addLayout(bbox)
        self.vbox.addWidget(self.setview)
        self.setLayout(self.vbox)
        self.setGeometry(QRect(1, 45, 496, 974))
        self.show()
        
    def __reduce_ex__(self,proto):
        return geneMyTreeWidget,(self.setview,)
        
    def save(self,other=False):
        if other: #self.filepath以外の保存先を指定する場合
            path = QFileDialog.getSaveFileName(None, 'chose save file','root.jh')[0]
            if not path=='': #pyqt5ではtapleの一個めにpathが入っている
                pickle.dump(self,open(path,'wb'))
                print('Saved To::')
                print(path)
        else: #default 
            pickle.dump(self,open(self.setview.filepath,'wb'))
            print('Saved To::')
            print(self.setview.filepath)
            
    def refresh(self):
        self.setview.resetView()
        self.cur=self.setview.cur
        self.setview.setmodel.mytree.currentSignal.connect(self.setCurrent)
        
    def setCurrent(self,mylist):
        self.cur=mylist[0]
        
def geneMyTreeView(model):
    return MyTreeView(model=model)

class MyTreeView(QTreeView):
    def __init__(self,model=None):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSortingEnabled( True )
#        self.setAlternatingRowColors(True)
#        self.setStyleSheet("background-color: rgb(55,62,75);alternate-background-color: rgb(44,48,60);\
#                           color: black;selection-color: yellow;selection-background-color: red;border: 1px solid white;\
#                           QTreeView::item:selected:active {border: 1px solid blue;}");
#        style='''
#            QTreeView::item:hover {border: 1px solid blue;background-color:rgba(116,169,214,100);border-style:none}
#            QTreeView::item:selected:active{background: rgba(116,169,214,10);border-style:none}
#            QTreeView::item:selected:!active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);border-style:none}
#            '''

        self.expanded.connect(self.showGraphs)
        self.collapsed.connect(self.showGraphs)
        if model==None:
            self.setmodel=MyTreeModel(MyTree.MyRootTree())
        else:
            self.setmodel=model
        self.cur=self.setmodel.mytree.current #mytreeのcurrentが常に入っている
        self.setmodel.mytree.currentSignal.connect(self.setCurrent)
        self.setModel(self.setmodel)
        self.doubleClicked.connect(self.setmodel.double_clicked)
        self.expandAll()
        self.setGeometry(QRect(1, 45, 496, 974))
        self.show()
        
    def __reduce_ex__(self,proto):
        #.dumpファイルは移動されるかもしれないのでpickle時にself.filepathは保存しない
        return geneMyTreeView,(self.model(),)
        
    def add(self,index=0):
        if 'folder'+str(index) in self.cur.getChildren().keys(): #同じ名前がある場合
            index+=1
            self.add(index)
        else:
            self.cur.add(MyTree.MyTree(),'folder'+str(index))
    
    def delete(self):
        selected=self.selectedIndexes()
        if len(selected)>0:
            index = self.selectedIndexes()[0]
            item=self.model().itemFromIndex(index)
            path=self.model().ascend(item)
            if len(path)>1: #['root']は消さない
                label=path.pop(-1)
                self.model().mytree.dele_this(path,label,signal=True)
        
    def setSavePath(self,filepath):
        self.filepath=filepath
        
    def setCurrent(self,mylist):
        self.cur=mylist[0]

    def resetView(self):
        #Viewとmytreeの間にずれが生じたときにmytreeに合わせてViewを初期化
        mytree=self.model().mytree
        self.setmodel=MyTreeModel(mytree)
        self.cur=self.setmodel.mytree.current #mytreeのcurrentが常に入っている
        self.setmodel.mytree.currentSignal.connect(self.setCurrent)
        self.setModel(self.setmodel)
        self.doubleClicked.connect(self.setmodel.double_clicked)
        return self
        
    def showGraphs(self,index):
        #表示するべきグラフの参照のリストを返す
        model=self.model()
        root=model.getRoot()
        open_graphs=self.getOpenGraphs(root,model)
        close_graphs=self.getCloseGraphs(root,model)
        for g in open_graphs:
            g.show()
        for g in close_graphs:
            g.hide()
        
    def getOpenGraphs(self,item,model):
        #item以下にある表示するべきグラフを返すcollapseされているフォルダは調べない
        if self.isExpanded(model.indexFromItem(item))==True:
            graphs=model.getGraphs(item) #直下のグラフ
            childItems=self.getChildren(item)
            for child in childItems:
                ref=model.getRef(child)
                if isinstance(ref,MyTree.MyTree):
                    graphs=graphs+self.getOpenGraphs(child,model)
            return graphs
        else:
            return []

    def getCloseGraphs(self,item,model):
        #item以下にある隠すべきグラフのリストを返す
        if self.isExpanded(model.indexFromItem(item))==True:
            graphs=[]
            childItems=self.getChildren(item)
            for child in childItems:
                ref=model.getRef(child)
                if isinstance(ref,MyTree.MyTree):
                    graphs=graphs+self.getCloseGraphs(child,model)
            return graphs
        else:
            return  self.getAllGraphs(item,model)
                    
    def getAllGraphs(self,item,model):
        #item以下にある全てのグラフのリストを返す
        graphs=model.getGraphs(item) #直下のグラフ
        childItems=self.getChildren(item)
        for child in childItems:
            ref=model.getRef(child)
            if isinstance(ref,MyTree.MyTree):
                graphs=graphs+self.getAllGraphs(child,model)
        return graphs
        
    @classmethod
    def getChildren(cls,item):
        childItems=[]
        for i in range(item.rowCount()):
            childItems.append(item.child(i,0))
        return childItems
        
    def save(self,other=False):
        if other: #self.filepath以外の保存先を指定する場合
            path = QFileDialog.getSaveFileName(None, 'chose save file','root.jh')[0]
            if not path=='': #pyqt5ではtapleの一個めにpathが入っている
                pickle.dump(self,open(path,'wb'))
                print('Saved To::')
                print(path)
        else: #default 
            pickle.dump(self,open(self.filepath,'wb'))
            print('Saved To::')
            print(self.filepath)

def geneMyTreeModel(tree):
    return MyTreeModel(tree)
        
class MyTreeModel(QStandardItemModel):
    deleSignal=pyqtSignal(list,str)
    pink=QColor(197,133,217)
    white=QColor(255,255,255)
    blue=QColor(97,175,239)
    green=QColor(148,194,115)
    def __init__(self,mytree):
        super().__init__(0,2)
        self.mytree=mytree
        self.mytree.addSignal.connect(self.add_to_model)
        self.mytree.deleSignal.connect(self.dele_from_model)
        self.mytree.renameSignal.connect(self.rename_model)
        
        self.setHeaderData( NAME,Qt.Horizontal, 'Name' )
        self.setHeaderData( TYPE,Qt.Horizontal, 'type' )
        self.containor=self.invisibleRootItem()
        self.containor.setDropEnabled(False)
        self.containor.appendRow(self.convert(mytree))
        
        #drag,dropに対応するために繋ぐが、mytreeからの操作があった時だけ一時的に切断する(mytreeに操作が反射するのを防ぐため)
        self.signalConnect()
        #GUI上のドラッグアンドドロップをmytreeに反映させるのに使う
        self.delePath=None
        self.deleLabel=None
        self.addPath=None
        self.addLabel=None
        
        #currentフォルダの背景色を変えるのに使う
        self.current=[]
        #currentフォルダへのアクセスに使う
        
        self.deleSignal.connect(self.dele_from_tree)
        
    def __reduce_ex__(self,proto):
        return geneMyTreeModel,(self.mytree,)
        
    def signalConnect(self):
        self.rowsRemoved.connect(self.remove, type=Qt.QueuedConnection)
        self.itemChanged.connect(self.changed)
        
    def signalDisconnect(self):
        self.rowsRemoved.disconnect(self.remove)
        self.itemChanged.disconnect(self.changed)
        
    def double_clicked(self,index):
        #TYPE上でダブルクリックされた時の動作を記述
        item=self.itemFromIndex(index)
        if item.column()==TYPE:
            ref=self.getRef(item)
            if isinstance(ref,MyTree.MyTree):
                #self.currentを更新してself.mytreeに反映　新旧のitemに通知
                pre=[]
                while len(self.current)>0:
                    pre.append(self.current.pop())
                for i in pre:
                    self.dataChanged.emit(self.indexFromItem(i),self.indexFromItem(i))
                self.current=self.getPaintRow(item)
                
                name=self.current[NAME]
                full_label=self.ascend(name)
                self.mytree.setCurrent(full_label)
                
                for i in self.current:
                    self.dataChanged.emit(self.indexFromItem(i),self.indexFromItem(i))
                    
            elif isinstance(ref,int):
                print(ref)
        
    def data(self, index, role =Qt.DisplayRole):
        #overriding method:indexで指定される要素に関する情報を返す
        if not index.isValid():
            return None
        else:
            item=self.itemFromIndex(index)
            
        if role ==Qt.DisplayRole:
            return item.text()
        elif role ==Qt.EditRole:
            return item.text()
        elif role ==Qt.BackgroundRole:
            if item in self.current:
                return self.pink
        elif role==Qt.ForegroundRole:
            if item in self.current:
                return self.white
            elif item.text()=='folder':
                return self.blue
            elif item.column()==1:
                return self.green
            else:
                return self.white
        else:
            return None
        
    def setData(self, index, value, role = Qt.EditRole):
        #overriding method:viewから編集された時の挙動を記述する
        if not index.isValid():
            return False
        item=self.itemFromIndex(index)
        if item.column()==NAME:
            full_label=self.ascend(item)
            if role ==Qt.EditRole and value != "":
                if item.parent()==None: #rootは変更不可
                    return False
                else:
                    try:
                        if self.mytree.rename_this(full_label,value):
                            self.mytree.rename_this(full_label,value)
                            item.setText(value)
                            return True
                        else:
                            return False
                    except:
                        return False
            else:
                return False
        else:
            return False
            
    def getRef(self,item):
        #itemの行のNAMEに対応するmytreeの参照を返す
        if item.parent()==None: #rootフォルダの場合
            return self.mytree
        else: 
            parent=item.parent()
            num=item.row()
            name=parent.child(num,NAME)
            full_path=self.ascend(name)
            return self.mytree.get_this(full_path)
            
    def getPaintRow(self,item):
        #カレントディレクトリとして色を変えて表示するitemのリストを返す
        if item.parent()==None: #rootフォルダの場合
            return [self.containor.child(0,i) for i in range(3)]
        else:
            parent=item.parent()
            num=item.row()
            return [parent.child(num,i) for i in range(3)]
          
    def convert(self,mytree):
        if not isinstance(mytree,MyTree.MyTree):
            print(mytree)
            raise TypeError('MyTree以外の変換は実装していません')
        else:
            folder=MyItemList(mytree.name,'folder')
            children=mytree.getChildren()
            for key,item in children.items():
                if isinstance(item,MyTree.MyTree): #子供がフォルダーの場合
                    folder.addChild(self.convert(item))
                else: #子供がデータだった場合
                    data=MyItemList(key,str(type(item)))
                    data[NAME].setDropEnabled(False)
                    folder.addChild(data)
            return folder
        
    def remove(self, index, first, last):
        #indexには除かれたアイテムの親のindexがはいる
        if index.isValid():
            parent = self.itemFromIndex(index)
            path=self.ascend(parent)
        self.delePath=path
        if not self.deleLabel==None:
            self.deleSignal.emit(self.delePath,self.deleLabel)
        
    def changed(self,item):
        #行が追加された時以外にも呼ばれるのでエラーの原因になるかも　今のところは大丈夫そう
        if item.column()==NAME and not item.parent()==None:
            self.deleLabel=item.text()
            self.addLabel=item.text()
            self.addPath=self.ascend(item.parent())
            
            if not self.delePath==None:
                self.deleSignal.emit(self.delePath,self.deleLabel)
                
    def dele_from_tree(self,path,label):
        addRef=self.mytree.dele_this(path,label)
        self.mytree.add_this(self.addPath,self.addLabel,addRef)
        self.delePath=None
        self.deleLabel=None
        
    def add_to_model(self,path,label,ref):
        #mytreeに追加された要素をmodelにも反映させる　refは長さ1のリスト mytreeへ重複した操作を反射しないようにするために一時的にシグナルを切る
        self.signalDisconnect()
        parent=self.pathToItem(path)
        target=ref[0]
        if isinstance(target,MyTree.MyTree): #子供がフォルダーの場合
            parent.appendRow(self.convert(target))
        else: #子供がデータだった場合
            data=MyItemList(label,str(type(target)))
            data[NAME].setDropEnabled(False)
            parent.appendRow(data)
        self.dataChanged.emit(self.indexFromItem(parent),self.indexFromItem(parent))
        self.signalConnect()
            
    def dele_from_model(self,path,label):
        #mytreeから削除された要素をmodelからも削除する
        self.signalDisconnect()
        parent=self.pathToItem(path)
        for i in range(parent.rowCount()):
            if parent.child(i,0).text()==label:
                parent.removeRow(i)
                break
        self.dataChanged.emit(self.indexFromItem(parent),self.indexFromItem(parent))
        self.signalConnect()
            
    def rename_model(self,path,before,after):
        #mytreeで改名された要素に対応するmodelの要素も改名する
        self.signalDisconnect()
        parent=self.pathToItem(path)
        for i in range(parent.rowCount()):
            if parent.child(i,0).text()==before:
                parent.child(i,0).setText(after)
                break
        self.dataChanged.emit(self.indexFromItem(parent),self.indexFromItem(parent))
        self.signalConnect()
        
    def pathToItem(self,path):
        #pathに対応するitemを返す
        start=self.getRoot()
        if path==['root']:
            return start
        else:
            for child in path[1:]:
                for i in range(start.rowCount()):
                    if start.child(i,0).text()==child:
                        start=start.child(i,0)
                        break
                    if i==start.rowCount()-1: #見つからない場合
                        raise Exception('pathで指定されたitemが見つかりません')
            return start
        
            
    def ascend(self,start):
        #startはQStandardItem invisibleRootからのパスを['root',....]のように返す
        path=[start.text()]
        while start.parent():
            start=start.parent()
            path.append(start.text())
        path.reverse()
        return path
        
    def getGraphs(self,item):
        #自身の直下（フォルダは展開しない）のグラフの参照のリストを返す
        import JupyterHuck5.MyGraph
        ref=self.getRef(item)
        if isinstance(ref,MyTree.MyTree):
            children=ref.getChildren()
            graphs=[]
            for child in children.values():
                if isinstance(child,MyGraphWindow):
                    graphs.append(child)
            return graphs
        else:
            return []
            
    def getRoot(self):
        #root itemを返す
        root=self.containor.child(0,0)
        return root
                 
class MyItemList(list):
    def __init__(self,*args):
        self.items=[QStandardItem(arg) for arg in args]
        for item in self.items[TYPE:]:
            item.setDropEnabled(False)
        self.items[TYPE].setEditable(False)
        super().__init__(self.items)
        self.children=[]

    def setDragEnabled(self,boolean):
        self.items[0].setDragEnabled(boolean)
        
    def addChild(self,itemlist):
        if isinstance(itemlist,MyItemList):
            self.items[0].appendRow(itemlist)
        else:
            raise TypeError('MyItemListしか追加できません')
            
if __name__=='__main__':
    app = QApplication( sys.argv )
    mw=MyTreeWidget()
    mytree=mw.cur
    folder1=MyTree.MyTree(children={'1_a':1.1,'1_b':'string','1_c':None})
    folder2=MyTree.MyTree(children={'2_a':1.1,'2_b':'string','2_c':None})
    folder3=MyTree.MyTree(children={'3_a':1.1,'3_b':'string','3_c':None})
    folder4=MyTree.MyTree(children={'4_a':1.1,'4_b':'string','4_c':None})
    folder3.add(folder4)
    folder2.add(folder3)
    folder1.add(folder2)
    mytree.add(folder1)
    sys.exit( app.exec_() )