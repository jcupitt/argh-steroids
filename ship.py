import os
import math
import random

import pygame
from pygame import mixer

import util
import sprite
import bullet
import alien
import asteroid

# default shield behavior 
# 0 is old regenerating shield behavior, 1 is manual shields
SHIELDMODE = 0

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
        self.jet_tick = 0
        self.shield_timer = 0
        self.shield_mode = SHIELDMODE
        self.engines = False

        self.fire_sound = mixer.Sound(os.path.join("sounds", "shot.ogg"))
        self.engine_sound = mixer.Sound(os.path.join("sounds", "engine.ogg"))
        self.fire_channel = pygame.mixer.Channel(2)
        self.engine_channel = pygame.mixer.Channel(1)

    def rotate_by(self, angle):
        self.angle += angle
        self.angle %= 360

    # power is a bool for thrust on or off
    def thrust(self, power):
        # engine state changed?
        if power != self.engines:
            if power:
                self.engine_channel.play(self.engine_sound, loops = -1)
            else:
                self.engine_channel.fadeout(500)
            self.engines = power

        if power:
            u = 0.1 * util.cos(self.angle)
            v = 0.1 * util.sin(self.angle)
            self.velocity = [self.velocity[0] + u, self.velocity[1] + v]
            
            self.jet_tick -= 1
            if self.jet_tick < 0:
                self.jet_tick = 3
                self.world.particle.jet(self.position, self.velocity, self.angle)

    def fire(self):
        if self.reload_timer == 0:
            self.fire_channel.stop()
            self.fire_channel.play(self.fire_sound)
            
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

        if self.shield_mode == 0:
            self.regenerate_timer = max(0, self.regenerate_timer - 1)
            if self.regenerate_timer == 0 and self.shields < self.max_shields:
                self.regenerate_timer = 500 
                self.shields += 1
        elif self.shield_mode == 1:
            self.shield_timer = max(0,self.shield_timer - 1)
            if self.shield_timer < 1 and self.shields > 0:
                self.shields -= 3

        super(Ship, self).update()

    # used for manual shields 
    def shield_on(self):
        if self.shield_mode == 1:
            if self.regenerate_timer == 0 and self.shields < self.max_shields:
                # change shield regeneration time below
                # actually regenerate time is  the difference
                # between "regenerate_timer" and "shield_timer"
                self.regenerate_timer = 1000 
                self.shields += 3
                if self.shields > 0:
                    self.shield_timer = 500 #change time shield is on here

    def impact(self, other):
        if isinstance(other, alien.Alien) or isinstance(other, asteroid.Asteroid):
            self.world.particle.sparks(self.position, self.velocity)
            self.shields -= 1
            self.regenerate_timer = 1000 
            if self.shields < 0:
                self.kill = True
                self.world.particle.explosion2(300, 
                                               self.position, self.velocity)

        super(Ship, self).impact(other)
    
    def draw(self):
        super(Ship, self).draw()

        for i in range(max(0, self.shields)):
            radius = int(self.scale + 5 + 4 * i)
            angle = ((i & 1) * 2 - 1) * self.shield_tick
            a = radius * util.cos(angle)
            b = radius * -util.sin(angle)
            c = -b
            d = a

            screen_points = [[int(a * x + b * y + self.position[0]), 
                              int(c * x + d * y + self.position[1])] 
                              for x, y in self.shield_points]

            for i in range(0, len(screen_points), 2):
                pygame.draw.line(self.world.surface, util.WHITE,
                                 screen_points[i], 
                                 screen_points[i + 1])

