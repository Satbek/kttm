import model
import random
import numpy as np

def test_getAccelerations(particles):
    solver = model.VerleSimpleSolver(time_step = 1, G = 1)
    assert solver._getAccelerations(particles) == [[3,3],[7,7],[-1.25, -1.25]]

def test_life_time(particles):
    time_interval = 10
    time_step = np.round(random.random(), 2)
    solvers = [
        model.OdeintSolver(time_step = time_step, G = 1),
        model.VerleSimpleSolver(time_step = time_step, G = 1)
    ]
    for solver in solvers:
        result = solver.solve(particles, time_interval)
        count = len(solver._get_times(time_interval))
        assert len(result) == count
        assert result[count - 1][0].life_time - time_step < time_step and \
            result[count - 1][1].life_time - time_step < 0 and \
            result[count - 1][2].life_time - time_step < 0

        life_time = result[0][0].life_time
        for i, particles in enumerate(result):
            assert particles[0].life_time == life_time - i * solver.time_step