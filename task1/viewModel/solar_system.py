from model import Particle as ModelPaticle
from viewModel.particle import Particle as ViewParticle
import numpy as np
def getSolarSystem():
    return {
        "Sun": ViewParticle(
            radius =  10 ** 10,
            model = ModelPaticle(
                x = 0,
                y = 0,
                mass = 1990000000000000000000000000000,
                speed_x=0,
                speed_y=0,
                life_time=np.inf,
            )
        ),
        "Merkury": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 58000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 48000,
                mass = 3.3e23,
            )
        ),
        "Venus": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 108000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 35000,
                mass = 4.87e24,
            )
        ),
        "Earth": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 150000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 30000,
                mass = 5.98e24,
            )
        ),
        "Mars": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 228000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 24000,
                mass = 6.42e23,
            )
        ),
        "Jupyter": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 778000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 13000,
                mass = 1.8999999999999998e27,
            )
        ),
        "Saturn": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 1427000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 9600,
                mass = 5.69e26,
            )
        ),
        "Uranus": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 2870000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 6800,
                mass = 8.68e25,
            )
        ),
        "Neptune": ViewParticle(
            radius = 10 ** 10,
            model = ModelPaticle(
                x = 4497000000000.0,
                y = 0,
                life_time = np.inf,
                speed_x = 0,
                speed_y = 5400,
                mass = 1.0199999999999999e26,
            )
        )
    }
