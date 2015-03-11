
import pygame
import math

import util

class Particles(object):
    def __init__(self, world):
        self.positions = []
        self.velocities = []
        self.life = []
        self.time = 0
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

            # tell the objects they have collided
            self.collide(other)

            break

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
        # need to update screen-space points
        self.transform()

        if self.continuous:
            pygame.draw.lines(self.world.surface, util.WHITE, True, 
                              self.screen_points)
        else:
            for i in range(0, len(self.screen_points), 2):
                pygame.draw.line(self.world.surface, util.WHITE, 
                                 self.screen_points[i], 
                                 self.screen_points[i + 1])

class World(object):
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.sprites = []
        self.world_map = []
        self.map_spacing = 100
        self.map_width = 1 + self.width / self.map_spacing
        self.map_height = 1 + self.height / self.map_spacing
        self.score = 0
        self.n_asteroids = 0

    def add(self, sprite):
        self.sprites.append(sprite)

    def remove_all(self):
        self.sprites = []
        self.n_asteroids = 0

    def update(self):
        for i in self.sprites:
            i.update()

        self.sprites = [x for x in self.sprites if not x.kill]

        self.world_map = []
        for x in range(self.map_width):
            map_row = [[] for y in range(self.map_height)]
            self.world_map.append(map_row)

        for i in self.sprites:
            i.tested_collision = False
            x = int(i.position[0] / self.map_spacing)
            y = int(i.position[1] / self.map_spacing)
            x_min = max(0, x - 1)
            x_max = min(self.map_width - 1, x + 1)
            y_min = max(0, y - 1)
            y_max = min(self.map_height - 1, y + 1)
            for a in range(x_min, x_max + 1):
                for b in range(y_min, y_max + 1):
                    self.world_map[a][b].append(i)

        for i in self.sprites:
            x = int(i.position[0] / self.map_spacing)
            y = int(i.position[1] / self.map_spacing)
            x = min(max(x, 0), self.map_width - 1)
            y = min(max(y, 0), self.map_height - 1)
            possible_sprites = self.world_map[x][y]
            i.test_collisions(possible_sprites)

            # now we've tested i against everything it could possibly touch, 
            # we no longer need to test anything against i
            i.tested_collision = True

    def draw(self):
        for i in self.sprites:
            i.draw()
