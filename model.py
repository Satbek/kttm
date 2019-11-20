import numpy as np
np.seterr('raise')
class Particle():
    def __init__(self, x, y,
        mass = 10, speed_x = 0, speed_y = 0, life_time = 10):
        self.x = x
        self.y = y
        self.mass = mass
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.life_time = life_time

    def __repr__(self):
        return "Particle[x = {x}, y = {y}, mass = {mass}, speed_x = {speed_x},\
speed_y = {speed_y}, life_time = {life_time}]".format(
        x = self.x,
        y = self.y,
        mass = self.mass,
        speed_x = self.speed_x,
        speed_y = self.speed_y,
        life_time = self.life_time
    )


class AbstractSolver():
    """
    Abstract Solver class
    """
    def __init__(self, time_step, G = 6.6743015 * (10 ** -11)):
        """
        G - gravity constant
        time_step - minimal indivisible time step
        """
        self.G = G
        self.time_step = time_step

    #todo cycles to numpy
    def _getAccelerations(self, particles):
        """
        returns array of accelerations
        [[acc_x, acc_y], [acc_x, acc_y], ...]
        """
        res = [0] * len(particles)
        for i, p_i in enumerate(particles):
            res[i] = [0, 0]
            for j, p_j in enumerate(particles):
                if j != i:
                    delta_x = p_j.x - p_i.x
                    delta_y = p_j.y - p_i.y
                    if delta_x != 0:
                        res[i][0] += \
                            self.G * p_j.mass * delta_x / np.abs(delta_x)**3
                    if delta_y != 0:
                        res[i][1] += \
                            self.G * p_j.mass * delta_y / np.abs(delta_y)**3
        return res

    def solve(self, particles, time_interval):
        """
        solves task
        returns array of particles arrays with len = time_interval // time_step
        [
            current_particles
            moved_particles,
            moved_particles,
            ....
        ]
        """
        raise("Not Implemented")


class VerleSimpleSolver(AbstractSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #todo cycles to numpy
    def solve(self, particles, time_interval):
        scenes_count = int(time_interval // self.time_step)
        result = []
        for scene_num in range(scenes_count):
            result.append([])
            for p in particles:
                new_particle = Particle(
                    p.x, p.y, p.mass, p.speed_x, p.speed_y,
                    p.life_time - (scene_num + 1) * self.time_step
                )
                result[scene_num].append(new_particle)
        result = [particles] + result
        for scene_num, _ in enumerate(result[:-1]):
            current_particles = result[scene_num - 1]
            current_accelerations = self._getAccelerations(current_particles)
            for i, p in enumerate(current_particles):
                result[scene_num + 1][i].x = p.x + p.speed_x * self.time_step \
                    + 0.5 * current_accelerations[i][0] * self.time_step

                result[scene_num + 1][i].y = p.y + p.speed_y * self.time_step \
                    + 0.5 * current_accelerations[i][1] * self.time_step

            future_accelerations = self._getAccelerations(result[scene_num])
            for i, p in enumerate(current_particles):
                result[scene_num + 1][i].speed_x = p.speed_x + 0.5 * \
                    (future_accelerations[i][0] + current_accelerations[i][0]) * \
                    self.time_step

                result[scene_num + 1][i].speed_y = p.speed_y + 0.5 * \
                    (future_accelerations[i][1] + current_accelerations[i][1]) * \
                    self.time_step
        return result

class VerleThreadingSolver(AbstractSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VerleMultiprocessingSolver(AbstractSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VerleCythonSolver(AbstractSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VerleOpenCLSolver(AbstractSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
