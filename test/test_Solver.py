import sys
import os
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import model

def test_getAccelerations():
    solver = model.AbstractSolver(time_step = 1, G = 1)
    p1 = model.Particle(x = 0, y = 0, mass = 1)
    p2 = model.Particle(x = 1, y = 1, mass = 1)
    p3 = model.Particle(x = 2, y = 2, mass = 8)
    assert solver.getAccelerations([p1, p2, p3]) == [[3,3],[7,7],[-1.25, -1.25]]

def test_VerleSimpleSolver():
    solver = model.VerleSimpleSolver(time_step = 1, G = 1)
    p1 = model.Particle(x = 0, y = 0, mass = 1, life_time = 10)
    p2 = model.Particle(x = 1, y = 1, mass = 1, life_time = 9)
    p3 = model.Particle(x = 2, y = 2, mass = 8, life_time = 8)
    particles = [p1, p2, p3]
    result = solver.solve(particles, 10)
    assert len(result) == 10
    assert len(result[9]) == 0
    assert len(result[8]) == 1
    assert len(result[7]) == 2
    assert len(result[6]) == 3

    assert result[0][0].x == 1.5
    assert result[0][0].y == 1.5

    assert result[0][1].x == 4.5
    assert result[0][1].y == 4.5

    assert result[0][2].x == 1.375
    assert result[0][2].y == 1.375

