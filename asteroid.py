
import pygame
import math
import random

import util
import sprite
import bullet
import ship
import alien

class Asteroid(sprite.Sprite):
    def __init__(self, world, scale, max_speed):
        super(Asteroid, self).__init__(world)
        world.n_asteroids += 1

        # spawn on a screen edge
        if random.randint(0, 1) == 0:
            x = random.randint(0, world.width)
            y = random.randint(0, 1) * world.height
        else:
            x = random.randint(0, 1) * world.width
            y = random.randint(0, world.height)
        self.position = [x, y] 

        n_points = random.randint(5, 10)
        self.points = []
        for i in range(n_points):
            angle = i * 360 / n_points + random.randint(-20, 20)
            distance = random.random() / 2.0 + 0.5
            self.points.append([distance * util.cos(angle), 
                                distance * util.sin(angle)])
        self.velocity = [random.random() * max_speed * 2 - max_speed, 
                         random.random() * max_speed * 2 - max_speed]
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

            # calculate point of impact for sparks
            dx = self.position[0] - other.position[0]
            dy = self.position[1] - other.position[1]
            d2 = dx * dx + dy * dy 
            d = math.sqrt(d2)
            if d == 0:
                d = 0.0001
            u = dx / d
            v = dy / d
            impact = [other.position[0] + u * other.scale,
                      other.position[1] + v * other.scale]
            self.world.particle.sparks(impact, other.velocity)

        super(Asteroid, self).collide(other)
