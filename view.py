import sys
import random
import numpy as np
import view_model
from PyQt5 import QtCore, QtWidgets, QtGui

class MainWidget(QtWidgets.QWidget):
    def buildEmitterLayout(self):
        self.emitter_vector_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.emitter_vector_slider.setRange(0, 360)
        self.emitter_vector_slider.setTickInterval(1)
        self.emitter_vector_slider.setSingleStep(1)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.emitter_vector_slider)

        double_validator = QtGui.QDoubleValidator(
            -10**9, 10**9, 3
        )
        self.particle_mass_line_edit = QtWidgets.QLineEdit()
        self.particle_mass_line_edit.setValidator(double_validator)
        self.particle_mass_line_edit.setText("10000000")

        self.particle_speed_x_line_edit = QtWidgets.QLineEdit()
        self.particle_speed_x_line_edit.setValidator(double_validator)
        self.particle_speed_x_line_edit.setText("0,0")

        self.particle_speed_y_line_edit = QtWidgets.QLineEdit()
        self.particle_speed_y_line_edit.setValidator(double_validator)
        self.particle_speed_y_line_edit.setText("0,0")

        layout.addWidget(self.particle_mass_line_edit)
        layout.addWidget(self.particle_speed_x_line_edit)
        layout.addWidget(self.particle_speed_y_line_edit)

        self.particle_life_time_line_edit = QtWidgets.QLineEdit()
        self.particle_life_time_line_edit.setValidator(double_validator)
        self.particle_life_time_line_edit.setText("10,0")

        layout.addWidget(self.particle_life_time_line_edit)
        return layout

    def buildInsrumentLayout(self):
        insrumentLayout = QtWidgets.QVBoxLayout()
        insrumentLayout.addLayout(self.buildEmitterLayout())
        self.spawn_particle_button = QtWidgets.QPushButton("Spawn particle")
        self.animation_start_button = QtWidgets.QPushButton("Start")
        self.animation_pause_button = QtWidgets.QPushButton("Pause")
        self.solar_system_button = QtWidgets.QPushButton("Solar System")
        self.clear_button = QtWidgets.QPushButton("Clear")
        insrumentLayout.addWidget(self.spawn_particle_button)
        insrumentLayout.addWidget(self.animation_start_button)
        insrumentLayout.addWidget(self.animation_pause_button)
        insrumentLayout.addWidget(self.clear_button)
        insrumentLayout.addWidget(self.solar_system_button)
        return insrumentLayout

    def buildView(self):
        scene = QtWidgets.QGraphicsScene()
        self.view = view_model.UniverseView(scene)
        return self.view

    def buildUI(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.buildView())
        self.layout.addLayout(self.buildInsrumentLayout())
        self.setLayout(self.layout)

    def buildConnections(self):
        self.emitter_vector_slider.valueChanged.connect(
            self.view.emitter.setVector
        )

        self.particle_mass_line_edit.textChanged.connect(
            self.view.emitter.setParticleMass
        )

        self.spawn_particle_button.clicked.connect(
            self.view.spawnParticle
        )

        self.particle_speed_x_line_edit.textChanged.connect(
            self.view.emitter.setParticleSpeedX
        )

        self.particle_speed_x_line_edit.textChanged.connect(
            self.view.emitter.setParticleSpeedX
        )

        self.particle_speed_y_line_edit.textChanged.connect(
            self.view.emitter.setParticleSpeedY
        )

        self.particle_life_time_line_edit.textChanged.connect(
            self.view.emitter.setParticleLifeTime
        )

        # self.solar_system_button.clicked.connect(
        #     self.view.addSolarSystem
        # )

        self.clear_button.clicked.connect(
            self.view.clear
        )

        self.animation_start_button.clicked.connect(
            self.view.startAnimation
        )

        self.animation_pause_button.clicked.connect(
            self.view.pauseAnimation
        )

    def __init__(self):
        super().__init__()
        self.buildUI()
        self.buildConnections()
