import math
from src.objects import CelestialObject, Asteroid


def test_asteroid_movement():
    planet = CelestialObject(0, 0, 100, None)
    asteroid = Asteroid(100, 0, 0, 0, 10, None)

    asteroid.move(planet)
    assert asteroid.x_pos < 100 
    assert asteroid.y_pos > 0