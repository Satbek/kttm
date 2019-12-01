import numpy as np
import math
from PyQt5 import QtCore, QtWidgets, QtGui
import model
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
from PyQt5.QtCore import (QObject, QPointF, 
        QPropertyAnimation, pyqtProperty)
import queue

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

class Particle(QObject):
    def __init__(self, radius, model):
        super().__init__()
        self.radius = radius
        self.item = QtWidgets.QGraphicsEllipseItem(
            QtCore.QRectF(-1 * radius, -1 * radius, 2 * radius, 2 * radius)
        )
        self.model = model
        self._set_pos(QtCore.QPointF(model.x, model.y))
    def _set_pos(self, pos):
        self.item.setPos(pos)
    pos = pyqtProperty(QPointF, fset=_set_pos)

class ParticleProcessor(QtCore.QThread):
    send_particles_signal = QtCore.pyqtSignal(list)
    def __init__(self, solver, time_interval, q_in):
        """
        solver - model_solver
        q_in - queue to get particles
        time_interval - time interval for solver
        """
        super().__init__()
        self.solver = solver
        self.time_interval = time_interval
        self.q_in = q_in

    def run(self):
        curr_particles = self.q_in.get()
        while True:
            if len(curr_particles) > 0:
                result = self.solver.solve(curr_particles, self.time_interval)
                self.send_particles_signal.emit(result)
            curr_particles = self.q_in.get()

class UniverseView(QtWidgets.QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.emitter = Emitter(10, 0, (10, 40))
        self.q_in_particles = queue.Queue()
        self.scene().addItem(self.emitter)
        self.time_step = 0.1
        self.time_interval = 1
        self.solver = model.VerleSimpleSolver(time_step = self.time_step)
        self._setup()

    def _setup(self):
        self.particles = []
        self.anim_group = QtCore.QSequentialAnimationGroup()
        self.anim_group.finished.connect(self.resetAnimation)
        self.anim_group.setLoopCount(1)
        self.particle_processor = ParticleProcessor(
            solver = self.solver,
            time_interval = self.time_interval,
            q_in = self.q_in_particles,
        )
        self.particle_processor.start()
        self.particle_processor.send_particles_signal.connect(self.applyAnimation)

    @staticmethod
    def mass2radius(mass):
        return math.log(float(mass), 6)

    def spawnParticle(self):
        """
        Spawn particle by Emitter
        """
        distance = np.random.randint(*self.emitter.spawnInterval)
        x = self.emitter.x() - (
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
        logging.info("Spawning particle with pos ({0},{1})".format(x, y))
        self.addParticle(particle)

    def addParticle(self, particle):
        self.particles.append(particle)
        self.scene().addItem(particle.item)

    def startAnimation(self):
        self.add_particles_to_processor()
        self.anim_group.start()
        self.particle_processor.start()

    def pauseAnimation(self):
        self.anim_group.pause()
        self.particle_processor.quit()

    def applyAnimation(self, particle_scenes):
        logging.info(
            "Applying animation, scenes count: {0}, particles count: {1}".format(
                len(particle_scenes),
                len(particle_scenes[0])
            )
        )
        logging.debug(
            "First particles start pos:({0},{1}), end pos:({2},{3})".format(
                np.round(particle_scenes[0][0].x,2), np.round(particle_scenes[0][0].y,2),
                np.round(particle_scenes[-1][0].x,2), np.round(particle_scenes[-1][0].y,2)
            )
        )
        for i, particles_scene in enumerate(particle_scenes[:-1]):
            sceneAnimation = QtCore.QParallelAnimationGroup()
            for j, v in enumerate(zip(particles_scene, self.particles)):
                model, particle = v
                particle_anim = QtCore.QPropertyAnimation(particle, b"pos")
                particle_anim.setDuration(self.time_step * 10**3)
                particle_anim.setStartValue(QPointF(model.x, model.y))
                particle_anim.setEndValue(
                    QPointF(
                        particle_scenes[i + 1][j].x,
                        particle_scenes[i + 1][j].y,
                    )
                )
                sceneAnimation.addAnimation(particle_anim)
            self.anim_group.addAnimation(sceneAnimation)

        for model, particle in zip(particle_scenes[-1], self.particles):
            particle.model = model
        self.anim_group.start()

    def add_particles_to_processor(self):
        """filter particles by lifetime, add them to queue"""
        filtered_particles = [p for p in self.particles if p.model.life_time > 0]
        for p in self.particles:
            if p.model.life_time <= 0:
                self.scene().removeItem(p.item)
        self.particles = filtered_particles
        self.q_in_particles.put([p.model for p in self.particles])

    def resetAnimation(self):
        self.anim_group.clear()
        self.add_particles_to_processor()

    def clear(self):
        for p in self.particles:
            self.scene().removeItem(p.item)
        self.anim_group.stop()
        self.anim_group = None
        self.particle_processor.quit()
        self._setup()

    def setSolver(self, action):
        solver_name = action.text()
        logging.info("Set {0} solver".format(solver_name))
        if solver_name == "Simple Verle":
            self.solver = model.VerleSimpleSolver(time_step = self.time_step)
        elif solver_name == "ODEINT":
            self.solver = model.OdeintSolver(time_step = self.time_step)
        self.particle_processor.quit()
        self.particle_processor = ParticleProcessor(
            solver = self.solver,
            time_interval = self.time_interval,
            q_in = self.q_in_particles,
        )
        self.particle_processor.start()
        self.particle_processor.send_particles_signal.connect(self.applyAnimation)