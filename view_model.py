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

class UniverseView(QtWidgets.QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.emitter = Emitter(10, 0, (10, 40))
        self.q_in_particles = queue.Queue()
        self.scene().addItem(self.emitter)
        self.time_step = 10**4
        self.time_interval = 10**5
        self.solver = model.VerleSimpleSolver(time_step = self.time_step)
        self.scale_factor = 1
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
                particle_anim.setDuration(self.time_step * 10 **-3)
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

    def addSolarSystem(self):
        self.clear()
        #sun
        self.scale_factor = 9 * 10**-10
        self.addParticle(
            Particle(
                radius = 2 * 10 ** 10,
                model = model.Particle(
                    x = 0,
                    y = 0,
                    mass = 1990000000000000000000000000000,
                    speed_x=0,
                    speed_y=0,
                    life_time=np.inf,
                )
            )
        )

        #Merkury
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 58000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 48000,
                    mass = 3.3e23,
                )
            )
        )

        #Venus
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 108000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 35000,
                    mass = 4.87e24,
                )
            )
        )

        #Earth
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 150000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 30000,
                    mass = 5.98e24,
                )
            )
        )

        #Mars
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 228000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 24000,
                    mass = 6.42e23,
                )
            )
        )

        #Jupyter
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 778000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 13000,
                    mass = 1.8999999999999998e27,
                )
            )
        )

        #Saturn
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 1427000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 9600,
                    mass = 5.69e26,
                )
            )
        )

        #Uranus
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 2870000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 6800,
                    mass = 8.68e25,
                )
            )
        )

        #Neptune
        self.addParticle(
            Particle(
                radius = 0.5 * 10 ** 10,
                model = model.Particle(
                    x = 4497000000000.0,
                    y = 0,
                    life_time = np.inf,
                    speed_x = 0,
                    speed_y = 5400,
                    mass = 1.0199999999999999e26,
                )
            )
        )

        self.scale(self.scale_factor, self.scale_factor)
        self.emitter.setScale(1 / self.scale_factor)
        self.emitter.setPos(0, 100)