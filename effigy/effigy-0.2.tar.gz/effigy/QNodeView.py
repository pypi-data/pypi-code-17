from PyQt5.QtWidgets import QGraphicsView


class QNodeView(QGraphicsView):
    def __init__(self, *__args):
        super().__init__(*__args)

        self.setDragMode(QGraphicsView.RubberBandDrag)