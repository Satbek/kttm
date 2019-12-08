from PyQt5 import QtCore, QtWidgets, QtGui

class Particle(QtCore.QObject):
    def __init__(self, radius, model, color = QtGui.QColor("black")):
        super().__init__()
        self.radius = radius
        self.item = QtWidgets.QGraphicsEllipseItem(
            QtCore.QRectF(-1 * radius, -1 * radius, 2 * radius, 2 * radius)
        )
        self.item.setBrush(color)
        self.model = model
        self._set_pos(QtCore.QPointF(model.x, model.y))

    def _set_pos(self, pos):
        self.item.setPos(pos)

    pos = QtCore.pyqtProperty(QtCore.QPointF, fset=_set_pos)
