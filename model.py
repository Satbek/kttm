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

    def getAccelerations(self, particles):
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
        returns modified particles
        returns array of particles arrays with len = time_interval // time_step
        [
            particles,
            particles,
            ....
        ]
        """
        raise("Not Implemented")


class VerleSimpleSolver(AbstractSolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def solve(self, particles, time_interval):
        scenes_count = time_interval // self.time_step
        result = []
        for scene_num in range(scenes_count):
            result.append([])
            for p in particles:
                if p.life_time - (scene_num + 1) * self.time_step > 0:
                    new_particle = Particle(
                        p.x, p.y, p.mass, p.speed_x, p.speed_y,
                        p.life_time - (scene_num + 1) * self.time_step
                    )
                    result[scene_num].append(new_particle)
        result = [particles] + result

        for scene_num, _ in enumerate(result[1:]):
            current_particles = result[scene_num-1]
            current_accelerations = self.getAccelerations(current_particles)
            for i, p in enumerate(current_particles):
                if i < len(result[scene_num]):
                    result[scene_num][i].x = p.x + p.speed_x * self.time_step \
                        + 0.5 * current_accelerations[i][0] * self.time_step
                    result[scene_num][i].y = p.y + p.speed_y * self.time_step \
                        + 0.5 * current_accelerations[i][1] * self.time_step

            future_accelerations = self.getAccelerations(current_particles)
            for i, p in enumerate(current_particles):
                if i < len(result[scene_num]):
                    result[scene_num][i].speed_x = p.speed_x + 0.5 * \
                        (future_accelerations[i][0] + current_accelerations[i][0]) * \
                        self.time_step

                    result[scene_num][i].speed_y = p.speed_y + 0.5 * \
                        (future_accelerations[i][1] + current_accelerations[i][1]) * \
                        self.time_step
        return result[1:]

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
