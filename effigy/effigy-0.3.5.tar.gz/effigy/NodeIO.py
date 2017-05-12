from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPathItem, QUndoCommand, QGraphicsItem
from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QTransform, QBrush, QColor, QPainterPath, QPen
from PyQt5.QtWidgets import QUndoCommand


from enum import Enum
import uuid

#from effigy.NodeLink import NodeLink, InvalidLinkException

class NodeIODirection(Enum):
    """Establish if IO direction is input, output or any"""
    any = 0
    output = 1
    input = 2

class NodeIOMultiplicity(Enum):
    """Whether the node can be connected to multiple other nodes, or just one"""
    single = 0
    multiple = 1

class NodeIO(QGraphicsItem):
    """General Input and Output class for Node links.

    This class builds the basis for inputs and outputs for nodes. You link nodes together via those inputs and outputs,
    and all IO must be typed. Only compatible IO (that is, IO of same type) can be linked together. Compatibility is
    established with the 'isinstance' method. Each IO has a direction, i.e. input, output or any. Inputs may only be
    conected with inputs (and 'any' of course), and vice versa."""

    # Direction for this class
    classDirection = NodeIODirection.any
    # Multiplicity for this class
    classMultiplicity = NodeIOMultiplicity.multiple


    def __init__(self, iotype, name, displaystr=None, setID=None, *args, **kwargs):
        if type(iotype) is not type:
            raise TypeError("iotype argument is of type '%s', but must be of type 'type'." % type(iotype))

        super().__init__(*args, **kwargs)

        self.iotype = iotype
        self.iodirection = NodeIO.classDirection

        if setID is not None:
            self.id = setID  # Unique ID to identify io across multiple sessions.
        else:
            self.id = uuid.uuid4().int

        self.name = str(name)   # Each IO needs a name unique across all instances of the node class using it
        self.displaystring = displaystr     # Preferred String to display next to IO when rendering. Not required for it to work.

        self.addGraphicsItems()

        self.nodeLinks = []
        self.tempNodeLink = None

    # Define a bounding rect for collision detection (needed for interacting with the IO)
    def boundingRect(self):
        return self.backgroundItem.rect()

    def addGraphicsItems(self):
        """Add Items to draw the IO pin. Can be overridden for custom graphics"""
        self.backgroundItem = QGraphicsRectItem(QRectF(-5, -5, 10, 10), self)

    def paint(self, *__args):
        """Must be defined, but as this is just a container item, it doesn't actually paint anything."""
        pass

    def deleteLink(self, link):
        link.startIO.nodeLinks.remove(link)
        link.endIO.nodeLinks.remove(link)
        self.scene().removeItem(link)

    def recursiveIOCheck(self, item):
        """Recursively check if item is a child of an IO item"""
        if item is None:  # We reached the topmost item
            return None
        if isinstance(item, NodeIO):  # Found a NodeIO
            return item
        else:
            return self.recursiveIOCheck(item.parentItem())  # We must go deeper and deeper!

    class DeleteLinkCommand(QUndoCommand):
        def __init__(self, io):
            super().__init__()
            self.io = io
            self.linkIOs = []
            self.scene = io.scene()

            for link in io.nodeLinks:
                self.linkIOs.append([link.startIO, link.endIO, link])

        def redo(self):
            for linkIO in self.linkIOs:
                linkIO[0].deleteLink(linkIO[2])

        def undo(self):
            for linkIO in self.linkIOs:
                linkIO[0].nodeLinks.append(linkIO[2])
                linkIO[1].nodeLinks.append(linkIO[2])

                self.scene.addItem(linkIO[2])


    class CreateLinkCommand(QUndoCommand):
        def __init__(self, startIO, endIO, scene, *args, **kwargs):
            self.startIO = startIO
            self.endIO = endIO
            self.scene = scene

            self.link = None

            self.firstredo = True

            super().__init__(*args, **kwargs)

        def redo(self):
            if not self.firstredo:
                self.link.startIO.nodeLinks.append(self.link)
                self.link.endIO.nodeLinks.append(self.link)
            else:
                self.link = NodeLink(startIO=self.startIO, endIO=self.endIO, undostack=self.scene.undostack)
                self.firstredo = False

            self.link.updateBezier()
            self.scene.addItem(self.link)

        def undo(self):
            self.startIO.deleteLink(self.link)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if QGraphicsSceneMouseEvent.button() == Qt.LeftButton:
            self.scene().undostack.beginMacro("Link Nodes")
            if type(self).classMultiplicity == NodeIOMultiplicity.single:
                if self.nodeLinks:
                    self.scene().undostack.push(NodeIO.DeleteLinkCommand(self))

            if self.tempNodeLink is None:
                if self.classDirection == NodeIODirection.input:
                    # On inputs, io is the ending point of bezier curve
                    self.tempNodeLink = NodeLink(startIO=None, endIO=self)
                else:
                    # Everywhere else, io is start point of bezier curve
                    self.tempNodeLink = NodeLink(startIO=self, endIO=None)
                self.scene().addItem(self.tempNodeLink)


    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        # update temporary link
        if self.tempNodeLink is not None:
            if self.classDirection == NodeIODirection.input:
                self.tempNodeLink.updateBezier(overrideStartpos=QGraphicsSceneMouseEvent.scenePos())
            else:
                self.tempNodeLink.updateBezier(overrideEndpos=QGraphicsSceneMouseEvent.scenePos())

    def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
        if QGraphicsSceneMouseEvent.button() == Qt.LeftButton:
            if self.tempNodeLink is None:
                return

            #  Delete temporary link
            self.scene().removeItem(self.tempNodeLink)
            self.tempNodeLink = None

            # Try to find any item at end coordinates
            endpos = QGraphicsSceneMouseEvent.scenePos()
            itematendpos = self.scene().itemAt(endpos, QTransform())

            # Check if item is nodeIO
            enditem = self.recursiveIOCheck(itematendpos)
            if enditem is not None:
                try:
                    # Check if IO directions are compatible
                    if self.classDirection == enditem.classDirection and not self.classDirection == NodeIODirection.any and not enditem.classDirection == NodeIODirection.any:
                        raise InvalidLinkException
                    if self.classDirection == NodeIODirection.input:
                        # On inputs, io is the ending point of bezier curve
                        linkAction = NodeIO.CreateLinkCommand(startIO=enditem, endIO=self, scene=self.scene())
                        self.scene().undostack.push(linkAction)
                    else:
                        # Everywhere else, io is start point of bezier curve
                        linkAction = NodeIO.CreateLinkCommand(startIO=self, endIO=enditem, scene=self.scene())
                        self.scene().undostack.push(linkAction)
                except InvalidLinkException:
                    pass

            else:   # No node found. Launch the module selector to spawn a compatible node
                self.scene().undostack.beginMacro("Create node from link")
                if self.classDirection == NodeIODirection.input:
                    returnio = self.scene().moduleManager.selectNode(QGraphicsSceneMouseEvent.pos(), inType=self.iotype)
                    if issubclass(type(returnio), NodeIO):
                        linkAction = NodeIO.CreateLinkCommand(startIO=returnio, endIO=self, scene=self.scene())
                        self.scene().undostack.push(linkAction)
                else:
                    returnio = self.scene().moduleManager.selectNode(QGraphicsSceneMouseEvent.pos(), outType=self.iotype)
                    if issubclass(type(returnio), NodeIO):
                        linkAction = NodeIO.CreateLinkCommand(startIO=self, endIO=returnio, scene=self.scene())
                        self.scene().undostack.push(linkAction)
                self.scene().undostack.endMacro()
            self.scene().undostack.endMacro()
        elif QGraphicsSceneMouseEvent.button() == Qt.RightButton:
            self.scene().undostack.push(NodeIO.DeleteLinkCommand(self))




class NodeInput(NodeIO):
    """General Input class for Node links. See NodeIO class for more information."""
    classDirection = NodeIODirection.input
    classMultiplicity = NodeIOMultiplicity.multiple

class NodeOutput(NodeIO):
    """General Output class for Node links. See NodeIO class for more information."""
    classDirection = NodeIODirection.output
    classMultiplicity = NodeIOMultiplicity.single


class InvalidLinkException(Exception):
    pass


class DeleteLinkFromMultiplicityCommand(QUndoCommand):
    """Only use in combination of the "Link IO" macro from NodeIO"""
    def __init__(self, link):
        super().__init__()
        self.link = link
        self.scene = self.link.scene()

    def redo(self):
        self.link.startIO.nodeLinks.remove(self.link)
        self.link.endIO.nodeLinks.remove(self.link)
        self.scene.removeItem(self.link)

    def undo(self):
        self.link.startIO.nodeLinks.append(self.link)
        self.link.endIO.nodeLinks.append(self.link)
        self.scene.addItem(self.link)

class NodeLink(QGraphicsPathItem):
    def __init__(self, startIO=None, endIO=None, undostack=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.startIO = startIO
        self.endIO = endIO
        self.undostack = undostack

        # Connections with yourself are not allowed
        if startIO == endIO:
            raise InvalidLinkException("startIO (ID: %s) and endIO (ID: %s) can not be the same!" % (startIO.id, endIO.id))

        if startIO is not None and endIO is not None:
            # Start type can be casted to end type
            if issubclass(startIO.iotype, endIO.iotype):

                # Remove duplicates
                for link in self.startIO.nodeLinks:
                    if link.startIO == self.startIO and link.endIO == self.endIO:
                        self.startIO.nodeLinks.remove(link)

                # Remove all other links if multiplicity calls for it
                if type(self.startIO).classMultiplicity == NodeIOMultiplicity.single:
                    for link in self.startIO.nodeLinks:
                        self.undostack.push(DeleteLinkFromMultiplicityCommand(link))
                self.startIO.nodeLinks.append(self)

                # Remove all other links if multiplicity calls for it
                if type(self.endIO).classMultiplicity == NodeIOMultiplicity.single:
                    for link in self.endIO.nodeLinks:
                        self.undostack.push(DeleteLinkFromMultiplicityCommand(link))
                self.endIO.nodeLinks.append(self)

    def updateBezier(self, overrideStartpos=QPointF(0, 0), overrideEndpos=QPointF(0, 0)):
        path = QPainterPath()

        if self.startIO is not None:
            startpos = self.startIO.scenePos()
        else:
            startpos = overrideStartpos

        if self.endIO is not None:
            endpos = self.endIO.scenePos()
        else:
            endpos = overrideEndpos

        path.moveTo(startpos)

        controlpoint = QPointF(abs((endpos - startpos).x()) * 0.8, 0)
        path.cubicTo(startpos + controlpoint,
                     endpos - controlpoint,
                     endpos)

        self.setPath(path)

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            self.setPen(QPen(Qt.red))
        else:
            self.setPen(QPen(Qt.black))
        painter.setPen(self.pen())
        painter.drawPath(self.path())
