import sys
import os
import model
import pytest
import random
import numpy as np

def test_Solve(particles):
    solver = model.OdeintSolver(time_step = 1, G = 1)
    result = solver.solve(particles, 10)
    eps = 10**-5
    assert result[1][0].x - 1.5 < eps
    assert result[1][0].y - 1.5 < eps

    assert result[1][1].x - 4.5 < eps
    assert result[1][1].y - 4.5 < eps

    assert result[1][2].x - 1.375 < eps
    assert result[1][2].y - 1.375 < eps

