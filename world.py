
import math
import random

import pygame

import util
import sprite
import particle
import text
import alien
import ship
import asteroid

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

        # input state
        self.quit = False
        self.rotate_left = False
        self.rotate_right = False
        self.rotate_by = 0
        self.thrust = False
        self.info = False
        self.fire = False
        self.spawn = False
        self.show_particles = True
        self.enter = False
        self.next_level = False

        # the ship ... or none for no ship on screen
        self.player = None

        # countdown timer until next alien
        self.alien_time = random.randint(1000, 2000)

    def n_objects(self):
        return len(self.sprites)

    def reset(self):
        self.sprites = []
        self.n_asteroids = 0
        self.particle.remove_all()
        self.text_y = 100
        self.score = 0
        self.player = None

    def remove_asteroids(self):
        self.sprites = [x for x in self.sprites 
                        if not isinstance(x, asteroid.Asteroid)]

    def add(self, sprite):
        self.sprites.append(sprite)

    def add_player(self):
        if not self.player:
            self.player = ship.Ship(self)

    def add_text(self, string, scale = 10):
        text.Character.string(self, string, 
                              [self.width / 2, self.text_y], scale)
        self.text_y += scale * 10

    def update(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self.quit = True 

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_LEFT:
                    self.rotate_left = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RIGHT:
                    self.rotate_right = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_UP:
                    self.thrust = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_SPACE:
                    self.fire = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_s:
                    self.spawn = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_n:
                    self.next_level = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_p:
                    if event.type == pygame.KEYDOWN:
                        self.show_particles = not self.show_particles
                elif event.key == pygame.K_i:
                    self.info = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RETURN:
                    self.enter = event.type == pygame.KEYDOWN
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.thrust = event.type == pygame.MOUSEBUTTONDOWN
                elif event.button == 1:
                    self.fire = event.type == pygame.MOUSEBUTTONDOWN

        self.particle.show(self.show_particles)

        x, y = pygame.mouse.get_rel()
        self.rotate_by = x / 5.0

        if self.rotate_left:
            self.rotate_by = -3
        elif self.rotate_right:
            self.rotate_by = 3

        if self.player:
            if self.thrust:
                self.player.thrust();

            if self.fire:
                self.player.fire();

            self.player.rotate_by(self.rotate_by)

        for i in self.sprites:
            i.update()
        self.particle.update()

        self.alien_time -= 1
        if self.alien_time < 0:
            self.alien_time = random.randint(1000, 2000)
            alien.Alien(self)

        if self.player and self.player.kill:
            self.player = None

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
