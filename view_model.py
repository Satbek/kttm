import numpy as np
import math
from PyQt5 import QtCore, QtWidgets, QtGui
import model

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

    def setVector(self, degree):
        self.degree = degree
        self.arrow.setRotation(degree)

    def setParticleMass(self, mass):
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

class Particle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, radius, model):
        super().__init__(
            QtCore.QRectF(-1 * radius, -1 * radius, 2 * radius, 2 * radius)
        )
        self.radius = radius
        self.model = model
        self.setPos(model.x, model.y)

class UniverseView(QtWidgets.QGraphicsView):
    emitter_x_changed_signal = QtCore.pyqtSignal(str)
    emitter_y_changed_signal = QtCore.pyqtSignal(str)
    def __init__(self, scene):
        super().__init__(scene)
        self._setup()

    def _setup(self):
        self.emitter = Emitter(10, 0, (10, 40))
        self.scene().addItem(self.emitter)
        self.particles = []

    @staticmethod
    def mass2radius(mass):
        return math.log(float(mass), 6)

    def spawnParticle(self):
        """
        Spawn particle by Emitter
        """
        distance = np.random.randint(*self.emitter.spawnInterval)
        x = self.emitter.x() + (
                self.emitter.radius + distance
            ) * np.sin(np.deg2rad(self.emitter.degree))
        
        y = self.emitter.y() + (
                self.emitter.radius + distance
            ) * np.cos(np.deg2rad(self.emitter.degree))
        particle = Particle(
            self.mass2radius(self.emitter.particleMass),
            model.Particle(
                x,
                y,
                self.emitter.particleMass,
                self.emitter.particle_speed_x,
                self.emitter.particle_speed_y,
                self.emitter.particle_life_time
            )
        )
        self.addParticle(particle)

    def addParticle(self, particle):
        self.particles.append(particle)
        self.scene().addItem(particle)

    def clear(self):
        self.scene().clear()
        self._setup()

    def addSolarSystem(self):
        self.clear()
        Sun = Particle(
            self.mass2radius(1990000000000.0),
            model.Particle(
                x = 0,
                y = 0,
                mass = 1990000000000.0,
                speed_x = 0,
                speed_y = 0,
                life_time = 10**6
            )
        )
        self.addParticle(Sun)

        Mercury = Particle(
            self.mass2radius(3.3 * 10 ** 5),
            model.Particle(
                x = 58.0,
                y = 0,
                mass = 3.3 * 10 ** 5,
                speed_x = 0,
                speed_y = 48000,
                life_time = 10**6
            )
        )
        self.addParticle(Mercury)

        Venus = Particle(
            self.mass2radius(4.87e6),
            model.Particle(
                x = 108.0,
                y = 0,
                mass = 4.87e6,
                speed_x = 0,
                speed_y = 35000,
                life_time = 10**6
            )
        )
        self.addParticle(Venus)

        Earth = Particle(
            self.mass2radius(5.98e6),
            model.Particle(
                x = 150.0,
                y = 0,
                mass = 5.98e6,
                speed_x = 0,
                speed_y = 30000,
                life_time = 10**6,
            )
        )
        self.addParticle(Earth)

        Mars = Particle(
            self.mass2radius(6.42e5),
            model.Particle(
                x = 228,
                y = 0,
                mass = 6.42e5,
                speed_x = 0,
                speed_y = 24000,
                life_time = 10**6,
            )
        )
        self.addParticle(Mars)

        Jupyter = Particle(
            self.mass2radius(1.8999999999999998e9),
            model.Particle(
                x = 778.0,
                y = 0,
                mass = 1.8999999999999998e9,
                speed_x = 0,
                speed_y = 13000,
                life_time = 10**6,
            )
        )
        self.addParticle(Jupyter)

        Saturn = Particle(
            self.mass2radius(5.69e8),
            model.Particle(
                x = 1427,
                y = 0,
                mass = 5.69e8,
                speed_x = 0,
                speed_y = 9600,
                life_time = 10**6,
            )
        )
        self.addParticle(Saturn)

        Uranus = Particle(
            self.mass2radius(8.68e7),
            model.Particle(
                x = 2870,
                y = 0,
                mass = 8.68e7,
                speed_x = 0,
                speed_y = 6800,
                life_time = 10**6,
            )
        )
        self.addParticle(Uranus)

        Neptune = Particle(
            self.mass2radius(1.0199999999999999e8,),
            model.Particle(
                x = 4497,
                y = 0,
                mass = 1.0199999999999999e8,
                speed_x = 0,
                speed_y = 5400,
                life_time = 10**6,
            )
        )
        self.addParticle(Neptune)
