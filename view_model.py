import numpy as np
import math
from PyQt5 import QtCore, QtWidgets, QtGui
import model
import logging
from viewModel.emitter import Emitter
from viewModel.particle_processor import ParticleProcessor
from viewModel.particle import Particle
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
from PyQt5.QtCore import (QObject, QPointF, 
        QPropertyAnimation, pyqtProperty)
import queue
from viewModel.solar_system import getSolarSystem

class UniverseView(QtWidgets.QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setup()

    def setup(self):
        self.emitter = Emitter(10, 0, (10, 40))
        self.q_in_particles = queue.Queue()
        self.scene().addItem(self.emitter)
        self.time_step = 0.1
        self.time_interval = 1
        self.anim_time = self.time_step * 10 **3
        self.solver = model.VerleSimpleSolver(time_step = self.time_step)
        self.scale_factor = 1
        self.particles = []
        self.particle_processor = ParticleProcessor(
            solver = self.solver,
            time_interval = self.time_interval,
            q_in = self.q_in_particles,
        )
        self.particle_processor.send_particles_signal.connect(self.applyAnimation)
        self.anim_group = QtCore.QSequentialAnimationGroup()
        self.anim_group.finished.connect(self.resetAnimation)
        self.anim_group.setLoopCount(1)

    @staticmethod
    def mass2radius(mass):
        return mass

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
            radius = self.mass2radius(self.emitter.particleMass),
            model = model.Particle(
                x,
                y,
                self.emitter.particleMass,
                self.emitter.particle_speed_x,
                self.emitter.particle_speed_y,
                self.emitter.particle_life_time
            ),
            color = self.emitter.particle_color
        )
        logging.info("Spawning particle with pos ({0},{1})".format(x, y))
        self.addParticle(particle)

    def _scale_by_particle_radius(self, particle_radius):
        width = self.scene().itemsBoundingRect().width()
        height = self.scene().itemsBoundingRect().height()
        if particle_radius > width or particle_radius > height:
            logging.info(
                "Rescale view by particle: particle_radius = {0}, width = {1}, height = {2}".format(
                    particle_radius,
                    width,
                    height
                )
            )
            scale_step = 2.5 / particle_radius
            self.scale_factor *= scale_step
            self.scale(scale_step, scale_step)
            self.emitter.setScale(1 / self.scale_factor)

    def addParticle(self, particle):
        self.particles.append(particle)
        self._scale_by_particle_radius(particle.radius)
        self.scene().addItem(particle.item)

    def startAnimation(self):
        self.add_particles_to_processor()
        self.anim_group.start()
        self.particle_processor.start()

    def pauseAnimation(self):
        self.anim_group.pause()
        self.particle_processor.quit()

    def moveEmitterToCenter(self):
        self.emitter.setPos(self.mapToScene(self.viewport().rect().center()))

    def applyAnimation(self, particle_scenes):
        logging.info(
            "Applying animation, scenes count: {0}, particles count: {1}".format(
                len(particle_scenes),
                len(particle_scenes[0])
            )
        )
        logging.debug(
            "Start particles pos:{0},\n end particles pos:{1}".format(
                [(np.round(p.x, 2), np.round(p.y, 2)) for p in particle_scenes[0]],
                [(np.round(p.x, 2), np.round(p.y, 2)) for p in particle_scenes[-1]],
            )
        )
        for i, particles_scene in enumerate(particle_scenes[:-1]):
            sceneAnimation = QtCore.QParallelAnimationGroup()
            for j, v in enumerate(zip(particles_scene, self.particles)):
                model, particle = v
                particle_anim = QtCore.QPropertyAnimation(particle, b"pos")
                particle_anim.setDuration(self.anim_time)
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
        self.particles = []
        self.anim_group.stop()
        if self.scale_factor != 1:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)
            self.emitter.setScale(1)
            logging.info("Reset scaling, scale_factor = {0}, scene_width = {1}, scene_height = {2}".format(
                self.scale_factor,
                self.scene().width(),
                self.scene().height()
            ))
            self.scale_factor = 1
        self.centerOn(self.emitter)
        self.setDefaultTimeParams()
        self.restartParticleProcessor()

    def setDefaultTimeParams(self):
        self.time_step = 0.1
        self.time_interval = 1
        self.anim_time = self.time_step * 10 **3
        self.solver.time_step = self.time_step

    def restartParticleProcessor(self):
        self.particle_processor.quit()
        self.particle_processor.solver = self.solver
        self.particle_processor.time_interval = self.time_interval
        self.particle_processor.q_in = self.q_in_particles
        self.particle_processor.start()

    def setSolver(self, action):
        solver_name = action.text()
        logging.info("Set {0} solver".format(solver_name))
        if solver_name == "Simple Verle":
            self.solver = model.VerleSimpleSolver(time_step = self.time_step)
        elif solver_name == "ODEINT":
            self.solver = model.OdeintSolver(time_step = self.time_step)
        self.restartParticleProcessor()

    def addSolarSystem(self):
        self.clear()
        self.time_step = 10**4
        self.time_interval = 10**5
        self.anim_time = self.time_step * 10 ** -3
        self.solver.time_step = self.time_step
        heavenly_bodies = getSolarSystem()
        for heavenly_body in heavenly_bodies.values():
            self.addParticle(heavenly_body)
        self.restartParticleProcessor()
