
import pygame
import math

import util
import sprite
import particle
import text

class World(object):
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.sprites = []
        self.particle = particle.Particle(surface)
        self.world_map = []
        self.map_spacing = 100
        self.map_width = 1 + self.width / self.map_spacing
        self.map_height = 1 + self.height / self.map_spacing
        self.score = 0
        self.n_asteroids = 0
        self.text_y = 100

    def add(self, sprite):
        self.sprites.append(sprite)

    def text(self, string, scale = 10):
        text.Character.string(self, string, 
                              [self.width / 2, self.text_y], scale)
        self.text_y += scale * 10

    def reset(self):
        self.sprites = []
        self.n_asteroids = 0
        self.particle.remove_all()
        self.text_y = 100
        self.score = 0

    def update(self):
        for i in self.sprites:
            i.update()
        self.particle.update()

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
        self.particle.draw()
        for i in self.sprites:
            i.draw()
