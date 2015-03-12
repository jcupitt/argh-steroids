
import pygame
import math

import util

class Sprite(object):
    def __init__(self, world):
        self.world = world
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.points = []
        self.kill = False
        self.tested_collision = False
        self.continuous = True
        self.scale = 10
        self.angle = 0
        world.add(self)

    def test_collisions(self, possible_sprites):
        for other in possible_sprites:
            if other == self:
                continue
            if other.tested_collision:
                continue

            dx = self.position[0] - other.position[0]
            dy = self.position[1] - other.position[1]
            d2 = dx * dx + dy * dy 
            t = self.scale + other.scale
            t2 = t * t
            if d2 > t2:
                continue

            # unit vector
            d = math.sqrt(d2)
            if d == 0:
                d = 0.0001
            u = dx / d
            v = dy / d

            # amount of overlap
            overlap = d - t

            # displace by overlap in that direction
            other.position[0] += u * overlap 
            other.position[1] += v * overlap

            # tell the objects they have collided ... both objects need to be
            # told
            self.impact(other)
            other.impact(self)

            self.collide(other)

            break

    # this method is triggered for both objects involved in the collision ... do
    # asymmetric things like bullets blowing up aliens
    def impact(self, other):
        pass

    # this is triggered just once, so symmetric things happen in this
    def collide(self, other):
        # exchange velocities
        x = other.velocity[0]
        other.velocity[0] = self.velocity[0]
        self.velocity[0] = x

        x = other.velocity[1]
        other.velocity[1] = self.velocity[1]
        self.velocity[1] = x

    def update(self):
        self.position = [self.position[0] + self.velocity[0], 
                         self.position[1] + self.velocity[1]]
        self.position[0] %= self.world.width
        self.position[1] %= self.world.height

    def draw(self):
        a = self.scale * util.cos(self.angle)
        b = self.scale * -util.sin(self.angle)
        c = -b
        d = a

        screen_points = [[int(a * x + b * y + self.position[0]), 
                          int(c * x + d * y + self.position[1])] 
                         for x, y in self.points]

        if self.continuous:
            pygame.draw.lines(self.world.surface, util.WHITE, True, 
                              screen_points)
        else:
            for i in range(0, len(screen_points), 2):
                pygame.draw.line(self.world.surface, util.WHITE, 
                                 screen_points[i], 
                                 screen_points[i + 1])
