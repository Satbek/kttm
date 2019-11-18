import sys
import random
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui

#todo clean up

class Arrow(QtWidgets.QGraphicsLineItem):
    def __init__(self, x, y, radius, outerPoint):
        self.radius = radius
        self.start = QtCore.QPointF(x, y)
        AgngleCoef = self._getAngleCoef(outerPoint)
        super().__init__(
            x + radius * AgngleCoef[0],
            y + radius * AgngleCoef[1],
            x + 3 * radius * AgngleCoef[0],
            y + 3 * radius * AgngleCoef[1]
        )
        self.vector = self._makeVector(radius, AgngleCoef)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setTransformOriginPoint(
            x + radius * AgngleCoef[0],
            y + radius * AgngleCoef[1],
        )

    def mouseMoveEvent(self, event):
        self.setVector(event.pos())

    def setVector(self, outerPoint):
        AgngleCoef = self._getAngleCoef(outerPoint)
        x, y, radius = self.start.x(), self.start.y(), self.radius
        self.vector = self._makeVector(radius, AgngleCoef)
        self.setLine(
            x + radius * AgngleCoef[0],
            y + radius * AgngleCoef[1],
            x + 3 * radius * AgngleCoef[0],
            y + 3 * radius * AgngleCoef[1]
        )
        self.setTransformOriginPoint(
            x + radius * AgngleCoef[0],
            y + radius * AgngleCoef[1],
        )
    
    def _makeVector(self, radius, AgngleCoef):
        x, y = self.start.x(), self.start.y()
        return QtCore.QPointF(x + radius * AgngleCoef[0], y + radius * AgngleCoef[1])

    def _getAngleCoef(self, outerPoint):
        """
        Get sin, cos coeffs to draw line toward provided point
        """
        norm = np.sqrt(outerPoint.x()**2 + outerPoint.y()**2)
        norm_x = 1 if norm == 0 else outerPoint.x() / norm
        norm_y = 1 if norm == 0 else outerPoint.y() / norm
        return (norm_x, norm_y)


class Emitter(QtWidgets.QGraphicsEllipseItem):
    def _buildArrowPen(self):
        arrowPen = QtGui.QPen()
        arrowPen.setWidth(3)
        arrowPen.setBrush(QtCore.Qt.red)
        self.arrow.setPen(arrowPen)

    def _buildPen(self):
        selfPen = QtGui.QPen()
        selfPen.setWidth(3)
        selfPen.setBrush(QtCore.Qt.red)
        self.setPen(selfPen)

    def __init__(self, radius, vector):
        super().__init__(
            QtCore.QRectF(-1 * radius, -1 * radius, 2 * radius, 2 * radius)
        )
        self.radius = radius
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.arrow = Arrow(self.x(), self.y(), radius, vector)
        self.arrow.setParentItem(self)

        self._buildPen()
        self._buildArrowPen()

    def getVector(self):
        return self.arrow.vector


class Particle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, radius, vector):
        super().__init__(
            QtCore.QRectF(-1 * radius, -1 * radius, 2 * radius, 2 * radius)
        )
        self.radius = radius
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.arrow = Arrow(self.x(), self.y(), radius, vector)
        self.arrow.setParentItem(self)

    def setScale(self, param):
        super().setScale(param)

    def setColor(self):
        pass

    def getVector(self):
        return self.arrow.vector

class ParticleSizeSlider(QtWidgets.QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRange(0, 100)
        self.setTickInterval(0.5)
        self.setSingleStep(0.5)
        self.particle = None


class MainWidget(QtWidgets.QWidget):
    def _buildInsrumentLayout(self):
        insrumentLayout = QtWidgets.QVBoxLayout()
        spawn_button = QtWidgets.QPushButton("Spawn particle")
        spawn_button.clicked.connect(self.addParticle)

        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.Clear)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(spawn_button)
        buttons_layout.addWidget(clear_button)

        insrumentLayout.addLayout(buttons_layout)

        self.slider = ParticleSizeSlider(QtCore.Qt.Horizontal)
        self.slider.valueChanged.connect(self.resizeItems)
        insrumentLayout.addWidget(self.slider)
        
        return insrumentLayout

    QtCore.pyqtSlot(int)
    def resizeItems(self, value):
        for item in self.view.scene().selectedItems():
            item.setScale(value / 20)

    def addEmitter(self):
        emitter = Emitter(20, QtCore.QPoint(1, 1))
        self.emitter = emitter
        self.view.scene().addItem(emitter)

    def _buildView(self):
        scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(scene)
        self.addEmitter()

    @QtCore.pyqtSlot()
    def Clear(self):
        self.view.scene().clear()
        self.addEmitter()

    @QtCore.pyqtSlot()
    def addParticle(self):
        particle = Particle(self.baseParticleSize, QtCore.QPointF(1, 1))
        direction = self.emitter.getVector()
        shift = random.randint(5, 25)

        particle.setPos(
            self.emitter.x() + direction.x() * shift,
            self.emitter.y() + direction.y() * shift
        )
        self.view.scene().addItem(particle)

    def __init__(self):
        super().__init__()
        self.baseParticleSize = 10

        self.layout = QtWidgets.QHBoxLayout()

        self._buildView()
        self.layout.addWidget(self.view)

        self.layout.addLayout(self._buildInsrumentLayout())

        self.setLayout(self.layout)
