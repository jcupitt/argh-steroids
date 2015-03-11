
import pygame
import math
import random

import util
import sprite
import bullet
import ship

class Asteroid(sprite.Sprite):
    def __init__(self, world, scale):
        super(Asteroid, self).__init__(world)
        world.n_asteroids += 1

        self.position = [random.randint(0, world.width),
                         random.randint(0, world.height)]
        n_points = random.randint(5, 10)
        self.points = []
        for i in range(n_points):
            angle = i * 360 / n_points + random.randint(-20, 20)
            distance = random.random() / 2.0 + 0.5
            self.points.append([distance * util.cos(angle), 
                                distance * util.sin(angle)])
        self.velocity = [random.random() * 2 - 1, random.random() * 2 - 1]
        self.angle = 0
        self.scale = scale
        self.angular_velocity = random.random() * 4 - 2

    def update(self):
        self.angle += self.angular_velocity
        super(Asteroid, self).update()

    def collide(self, other):
        if isinstance(other, Asteroid):
            # exchange spins
            x = other.angular_velocity
            other.angular_velocity = self.angular_velocity
            self.angular_velocity = x

            super(Asteroid, self).collide(other)
        elif isinstance(other, bullet.Bullet) or isinstance(other, ship.Ship):
            # asteroids can collide with bullets or bullets with asteroids ...
            # handle these cases in the other classes
            other.collide(self)
