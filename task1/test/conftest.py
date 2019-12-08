import pytest
import model
@pytest.fixture
def particles():
    p1 = model.Particle(x = 0.0, y = 0.0, speed_x = 0.0, speed_y = 0.0, mass = 1.0)
    p2 = model.Particle(x = 1.0, y = 1.0, speed_x = 0.0, speed_y = 0.0, mass = 1.0)
    p3 = model.Particle(x = 2.0, y = 2.0, speed_x = 0.0, speed_y = 0.0, mass = 8.0)
    return [p1, p2, p3]