from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPathItem
from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPen

from enum import Enum

class NodeIODirection(Enum):
    """Establish if IO direction is input, output or any"""
    any = 0
    output = 1
    input = 2

class NodeIOMultiplicity(Enum):
    """Whether the node can be connected to multiple other nodes, or just one"""
    single = 0
    multiple = 1

class InvalidLinkException(Exception):
    pass

class NodeLink(QGraphicsPathItem):
    def __init__(self, startIO=None, endIO=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.startIO = startIO
        self.endIO = endIO

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
                        self.startIO.nodeLinks.remove(link)
                self.startIO.nodeLinks.append(self)

                # Remove all other links if multiplicity calls for it
                if type(self.endIO).classMultiplicity == NodeIOMultiplicity.single:
                    for link in self.endIO.nodeLinks:
                        self.endIO.nodeLinks.remove(link)
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
