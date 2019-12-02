from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

class Arrow(QtWidgets.QGraphicsLineItem):
    def __init__(self, x, y, radius, degree):
        self.radius = radius
        self.start = QtCore.QPointF(x, y)
        rad = np.deg2rad(degree)
        super().__init__(
            x + radius * np.sin(rad),
            y + radius * np.cos(rad),
            x + 3 * radius * np.sin(rad),
            y + 3 * radius * np.cos(rad)
        )


class Emitter(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, radius, degree, spawnInterval):
        """
        radius - emitter circle radius
        degree - arrow rotation degree (0, 360)
        spawnInterval - (a, b) interval. Between this interval emitter will
        spawn particle
        """
        super().__init__(
            QtCore.QRectF(-1 * radius, -1 * radius, 2 * radius, 2 * radius)
        )
        self.radius = radius
        self.degree = degree
        self.spawnInterval = spawnInterval
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.arrow = Arrow(self.x(), self.y(), radius, degree)
        self.arrow.setParentItem(self)
        self.particleMass = 10000000
        self.particle_speed_x = 0
        self.particle_speed_y = 0
        self.double_validator = QtGui.QDoubleValidator(
            -10**9, 10**9, 3
        )
        self.particle_life_time = 10
        self.setBrush(QtGui.QBrush(QtCore.Qt.red))

    def setVector(self, degree):
        logging.info("Rotate emitter vector, degree: {0}".format(degree))
        self.degree = degree
        self.arrow.setRotation(degree)

    def setParticleMass(self, mass):
        if self.double_validator.validate(mass, 0)[0] == QtGui.QValidator.Acceptable:
            self.particleMass = float(mass.replace(",", "."))

    def setParticleSpeedX(self, speed_x):
        if self.double_validator.validate(speed_x, 0)[0] == QtGui.QValidator.Acceptable:
            self.particle_speed_x = float(speed_x.replace(",", "."))

    def setParticleSpeedY(self, speed_y):
        if self.double_validator.validate(speed_y, 0)[0] == QtGui.QValidator.Acceptable:
            self.particle_speed_y = float(speed_y.replace(",", "."))

    def setParticleLifeTime(self, life_time):
        if self.double_validator.validate(life_time, 0)[0] == QtGui.QValidator.Acceptable:
            self.particle_life_time = float(life_time.replace(",", "."))
