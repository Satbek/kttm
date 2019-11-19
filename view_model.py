import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui

#todo via Qt transform
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

    def setVector(self, degree):
        rad = np.deg2rad(degree)
        x, y, radius = self.start.x(), self.start.y(), self.radius
        self.setLine(
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
        self.particleMass = 10
        self.particle_speed_x = 0
        self.particle_speed_y = 0
        self.double_validator = QtGui.QDoubleValidator(
            -10**9, 10**9, 3
        )
        self.particle_life_time = 10

    QtCore.pyqtSlot(int)
    def setVector(self, degree):
        self.degree = degree
        self.arrow.setVector(degree)

    QtCore.pyqtSlot(float)
    def setParticleMass(self, mass):
        self.particleMass = mass

    QtCore.pyqtSlot(float)
    def setParticleSpeedX(self, speed_x):
        if self.double_validator.validate(speed_x, 0)[0] == QtGui.QValidator.Acceptable:
            self.particle_speed_x = float(speed_x.replace(",", "."))

    QtCore.pyqtSlot(float)
    def setParticleSpeedY(self, speed_y):
        if self.double_validator.validate(speed_y, 0)[0] == QtGui.QValidator.Acceptable:
            self.particle_speed_y = float(speed_y.replace(",", "."))

    QtCore.pyqtSlot(float)
    def setParticleLifeTime(self, life_time):
        if self.double_validator.validate(life_time, 0)[0] == QtGui.QValidator.Acceptable:
            self.particle_life_time = float(life_time.replace(",", "."))

class Particle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, radius):
        super().__init__(
            QtCore.QRectF(-1 * radius, -1 * radius, 2 * radius, 2 * radius)
        )
        self.radius = radius

class UniverseView(QtWidgets.QGraphicsView):
    emitter_x_changed_signal = QtCore.pyqtSignal(str)
    emitter_y_changed_signal = QtCore.pyqtSignal(str)
    def __init__(self, scene):
        super().__init__(scene)
        self.emitter = Emitter(10, 0, (10, 40))
        self.scene().addItem(self.emitter)
        self.particles = []

    @staticmethod
    def mass2radius(mass):
        return mass

    QtCore.pyqtSlot()
    def addParticle(self):
        particle = Particle(self.mass2radius(self.emitter.particleMass))
        distance = np.random.randint(*self.emitter.spawnInterval)
        x = self.emitter.x() + (
                self.emitter.radius + distance
            ) * np.sin(np.deg2rad(self.emitter.degree))
        
        y = self.emitter.y() + (
                self.emitter.radius + distance
            ) * np.cos(np.deg2rad(self.emitter.degree))
        particle.setPos(x, y)
        self.particles.append(particle)
        self.scene().addItem(particle)