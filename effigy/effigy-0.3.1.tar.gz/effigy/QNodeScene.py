from PyQt5.QtWidgets import QGraphicsScene, QUndoStack, QUndoCommand
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform
from effigy.QNodeSceneNode import QNodeSceneNode
from effigy.NodeIO import NodeIO
from effigy.NodeLink import NodeLink

class NodeSceneModuleManager:
    def __init__(self):
        self.scene = None

    def selectNode(self, position, inType:type=None, outType:type=None):
        return None

class QNodeScene(QGraphicsScene):
    def __init__(self, moduleManager=None, *__args):
        self.undostack = QUndoStack()
        if moduleManager:
            self.moduleManager = moduleManager
        else:
            self.moduleManager = NodeSceneModuleManager()
        self.moduleManager.scene = self

        super().__init__(*__args)

        #self.mouseDoubleClickEvent.connect(self.mouseDoubleClickEvent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.undostack.undo()
        elif event.key() == Qt.Key_D:
            self.undostack.redo()
        elif event.key() == Qt.Key_Delete:
            self.delSelection()

    def delSelection(self):
        self.undostack.beginMacro("Delete Stuff")

        selectedItems = self.selectedItems()

        links = [x for x in selectedItems if issubclass(type(x), NodeLink)]
        nodes = [x for x in selectedItems if issubclass(type(x), QNodeSceneNode)]
        #remainder = [x for x in selectedItems if not issubclass(type(x), (QNodeSceneNode, NodeLink))]

        for link in links:
            self.undostack.push(type(link.startIO).DeleteLinkCommand(link.startIO))

        for node in nodes:
            for io in node.IO.values():
                self.undostack.push(type(io).DeleteLinkCommand(io))
            self.undostack.push(QNodeScene.DeleteNodeCommand(node))

        self.undostack.endMacro()

    class DeleteNodeCommand(QUndoCommand):
        def __init__(self, node):
            super().__init__()

            self.node = node
            self.scene = self.node.scene()

        def redo(self):
            self.scene.removeItem(self.node)

        def undo(self):
            self.scene.addItem(self.node)

    def mouseDoubleClickEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton and not self.itemAt(mouseEvent.scenePos(), QTransform()):
            self.moduleManager.selectNode(mouseEvent.scenePos())
