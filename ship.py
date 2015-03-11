
import math
import random

import pygame

import util
import sprite
import bullet
import alien
import asteroid

class Ship(sprite.Sprite):
    def __init__(self, world):
        super(Ship, self).__init__(world)

        self.position = [world.width / 2, 
                         world.height / 2]
        self.points = [[1, 0], 
                       [util.cos(140), util.sin(140)],
                       [-0.3, 0],
                       [util.cos(220), util.sin(220)]]
        self.shield_points = []
        for i in range(5):
            self.shield_points.append([util.cos(i * 360 / 5 - 15), 
                                       util.sin(i * 360 / 5 - 15)])
            self.shield_points.append([util.cos(i * 360 / 5 + 15), 
                                       util.sin(i * 360 / 5 + 15)])
        self.velocity = [0, 0]
        self.angle = 0
        self.scale = 5
        self.reload_timer = 0
        self.regenerate_timer = 0
        self.max_shields = 3
        self.shields = self.max_shields
        self.shield_tick = 0

    def rotate_right(self):
        self.angle += 3
        if self.angle > 360:
            self.angle -= 360

    def rotate_left(self):
        self.angle -= 3
        if self.angle < 0:
            self.angle += 360

    def rotate_by(self, angle):
        self.angle += angle
        self.angle %= 360

    def thrust(self):
        u = 0.02 * util.cos(self.angle)
        v = 0.02 * util.sin(self.angle)
        self.velocity = [self.velocity[0] + u, self.velocity[1] + v]

        self.world.particle.jet(self.position, self.velocity, self.angle)

    def fire(self):
        if self.reload_timer == 0:
            a = util.cos(self.angle)
            b = util.sin(self.angle)

            projectile = bullet.Bullet(self.world)
            projectile.position = [self.position[0] + self.scale * a,
                                   self.position[1] + self.scale * b]
            projectile.velocity = [a * 7.0 + self.velocity[0],
                                   b * 7.0 + self.velocity[1]]
            projectile.angle = self.angle

            self.reload_timer = 10

    def update(self):
        self.reload_timer = max(0, self.reload_timer - 1)
        self.shield_tick += 1

        self.regenerate_timer = max(0, self.regenerate_timer - 1)
        if self.regenerate_timer == 0 and self.shields < self.max_shields:
            self.regenerate_timer = 200 
            self.shields += 1

        super(Ship, self).update()

    def collide(self, other):
        if isinstance(other, alien.Alien) or isinstance(other, asteroid.Asteroid):
            self.world.particle.sparks(self.position, self.velocity)
            self.shields -= 1
            self.regenerate_timer = 1000 
            if self.shields < 0:
                self.kill = True
                self.world.particle.explosion2(200, 
                                               self.position, self.velocity)

        super(Ship, self).collide(other)

    def draw(self):
        super(Ship, self).draw()

        for i in range(max(0, self.shields)):
            radius = int(self.scale + 5 + 4 * i)
            angle = ((i & 1) * 2 - 1) * self.shield_tick
            a = radius * util.cos(angle)
            b = radius * -util.sin(angle)
            c = -b
            d = a

            screen_points = [[a * x + b * y + self.position[0], 
                              c * x + d * y + self.position[1]] 
                              for x, y in self.shield_points]

            for i in range(0, len(screen_points), 2):
                pygame.draw.line(self.world.surface, util.WHITE,
                                 screen_points[i], 
                                 screen_points[i + 1])

