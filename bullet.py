
import pygame
import math
import random

import util
import sprite
import asteroid
import alien

class Bullet(sprite.Sprite):
    def __init__(self, world):
        super(Bullet, self).__init__(world)

        self.points = [[1, 0], 
                       [util.cos(120), util.sin(120)],
                       [util.cos(240), util.sin(240)]]
        self.scale = 2
        self.life = 100
        self.angle = 0

    def update(self):
        super(Bullet, self).update()

        self.life -= 1
        if self.life == 0:
            self.kill = True

    def impact(self, other):
        if isinstance(other, alien.Alien):
            other.kill = True
            self.kill = True
            self.world.score += 1000
            self.world.particle.explosion(20, 
                                          other.position, other.velocity)
        elif isinstance(other, asteroid.Asteroid):
            other.kill = True
            self.kill = True
            self.world.score += other.scale
            self.world.n_asteroids -= 1
            self.world.particle.explosion(other.scale / 3, 
                                          other.position, other.velocity)

            if other.scale > 15:
                n = random.randint(2, max(2, min(5, other.scale / 5)))
                for i in range(n):
                    new_asteroid = asteroid.Asteroid(self.world, 
                                                     other.scale / n )
                    new_asteroid.position[0] = other.position[0]
                    new_asteroid.position[1] = other.position[1]
                    new_asteroid.velocity[0] += other.velocity[0]
                    new_asteroid.velocity[1] += other.velocity[1]
