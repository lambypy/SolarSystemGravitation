import math
import pygame
from settings import G


class CelestialObject:
    """Represents a celestial object with a position, mass, and representative image"""
    def __init__(self, x_pos, y_pos, mass, img):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.mass = mass
        self.img = img

    def draw(self, win):
        """Draws celestial object on the screen"""
        img_size = self.img.get_width() // 2
        win.blit(self.img, (self.x_pos - img_size, self.y_pos - img_size))


class Asteroid(CelestialObject):
    """Represents a moving asteroid"""
    def __init__(self, x_pos, y_pos, vel_x, vel_y, mass, img):
        super().__init__(x_pos, y_pos, mass, img)
        self.vel_x = vel_x
        self.vel_y = vel_y


    def move(self, planets):
        """Moves the asteroid under influence of one or more planets"""
        for planet in planets:
            distance = math.sqrt((self.x_pos - planet.x_pos)**2 + (self.y_pos - planet.y_pos)**2)
            # Avoiding division by 0
            if distance == 0: 
                continue

            force = (G * self.mass * planet.mass) / distance ** 2
            acceleration = force / self.mass
            angle = math.atan2(planet.y_pos - self.y_pos, planet.x_pos - self.x_pos)
            acceleration_x = acceleration * math.cos(angle)
            acceleration_y = acceleration * math.sin(angle)
            
            # Updates velocity
            self.vel_x += acceleration_x
            self.vel_y += acceleration_y

        # Updates position
        self.x_pos += self.vel_x
        self.y_pos += self.vel_y