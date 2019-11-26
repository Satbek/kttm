import sys
import os
import model
import pytest

@pytest.fixture
def particles():
    p1 = model.Particle(x = 0, y = 0, mass = 1)
    p2 = model.Particle(x = 1, y = 1, mass = 1)
    p3 = model.Particle(x = 2, y = 2, mass = 8)
    return [p1, p2, p3]

def test_getAccelerations(particles):
    solver = model.AbstractSolver(time_step = 1, G = 1)
    assert solver._getAccelerations(particles) == [[3,3],[7,7],[-1.25, -1.25]]

def test_VerleSimpleSolver_lifetime(particles):
    solver = model.VerleSimpleSolver(time_step = 1, G = 1)
    result = solver.solve(particles, 10)
    assert len(result) == 11
    assert result[10][0].life_time == 0 and result[10][1].life_time <= 0 and \
        result[10][2].life_time <= 0

def test_VerleSimpleSolver_get_coordinates(particles):
    solver = model.VerleSimpleSolver(time_step = 1, G = 1)
    result = solver.solve(particles, 10)
    assert result[0] == particles
    assert result[1][0].x == 1.5
    assert result[1][0].y == 1.5

    assert result[1][1].x == 4.5
    assert result[1][1].y == 4.5

    assert result[1][2].x == 1.375
    assert result[1][2].y == 1.375

