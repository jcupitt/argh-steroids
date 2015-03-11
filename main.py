#!/usr/bin/python

import random
import math

import pygame

import util
import ship
import asteroid
import alien
import sprite
import text
import world

class Game(object):
    def __init__(self, surface):
        self.surface = surface
        self.world = world.World(surface)
        self.width = self.world.width
        self.height = self.world.height
        self.clock = pygame.time.Clock()
        self.level = 1

        # input state
        self.quit = False
        self.rotate_left = False
        self.rotate_right = False
        self.rotate_by = 0
        self.thrust = False
        self.info = False
        self.fire = False
        self.spawn = False
        self.any_key = False

        # the ship ... or none for no ship on screen
        self.player = None

        # countdown timer until next alien
        self.alien_time = random.randint(1000, 2000)

    def scan_input(self):
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
                elif event.key == pygame.K_i:
                    self.info = event.type == pygame.KEYDOWN

                self.any_key = event.type == pygame.KEYDOWN

                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        thrust = event.type == pygame.MOUSEBUTTONDOWN
                    elif event.button == 1:
                        fire = event.type == pygame.MOUSEBUTTONDOWN

        x, y = pygame.mouse.get_rel()
        self.rotate_by = x / 5.0

        if self.rotate_left:
            self.rotate_by = -3
        elif self.rotate_right:
            self.rotate_by = 3

    def update_alien(self):
        self.alien_time -= 1
        if self.alien_time < 0:
            self.alien_time = random.randint(1000, 2000)
            alien.Alien(self.world)

    def start_screen(self):
        self.world.text('ARGH ITS THE ASTEROIDS', scale = 20)
        self.world.text('PRESS ESC TO QUIT') 
        self.world.text('PRESS LEFT AND RIGHT TO ROTATE') 
        self.world.text('PRESS UP FOR THRUST')
        self.world.text('PRESS SPACE FOR FIRE')
        self.world.text('OR USE MOUSE CONTROLS') 
        self.world.text('WATCH OUT FOR ALLEN THE ALIEN')
        self.world.text('ANY KEY TO START', scale = 20)

        for i in range(4):
            asteroid.Asteroid(self.world, random.randint(50, 100))

        while not self.quit and not self.any_key:
            self.scan_input()
            self.update_alien()
            self.world.update()

            self.surface.fill(util.BLACK)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def update_player(self):
        if self.player:
            if self.thrust:
                self.player.thrust();

            if self.fire:
                self.player.fire();

            self.player.rotate_by(self.rotate_by)

    def draw_hud(self):
        text.draw_string(self.surface, "SCORE %d" % self.world.score, 
                         util.WHITE, 10, [10, 20])
        text.draw_string(self.surface, "LEVEL %d" % self.level, 
                         util.WHITE, 10, [10, 40])

        if self.info:
            text.draw_string(self.surface, 
                             "FPS %d" % self.clock.get_fps(),
                             util.WHITE, 5, [10, self.height - 20])
            n_particles = self.world.particle.n_particles()
            n_sprites = len(self.world.sprites)
            text.draw_string(self.surface, 
                             "OBJECTS %d" % (n_particles + n_sprites),
                             util.WHITE, 5, [10, self.height - 30])

    def level_start(self):
        start_animation_frames = 100
        start_animation_time = start_animation_frames

        while not self.quit and start_animation_time > 0:
            self.scan_input()
            if self.spawn:
                asteroid.Asteroid(self.world, random.randint(50, 100))
            self.update_player()
            self.world.update()

            self.surface.fill(util.BLACK)
            self.draw_hud()
            start_animation_time -= 1
            t = float(start_animation_time) / start_animation_frames
            text.draw_string(self.surface, "LEVEL START", util.WHITE,
                             t * 150,
                             [self.width / 2, self.height / 2],
                             centre = True, 
                             angle = t * 200.0)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def play_level(self):
        while not self.quit and self.world.n_asteroids > 0 and not self.player.kill:
            self.scan_input()
            self.world.update()
            self.update_player()
            self.update_alien()

            self.surface.fill(util.BLACK)
            self.draw_hud()
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def game_over(self):
        end_animation_frames = 100
        end_animation_time = end_animation_frames

        while not self.quit and end_animation_time > 0:
            self.scan_input()
            self.world.update()

            self.surface.fill(util.BLACK)
            self.draw_hud()
            end_animation_time -= 1
            t = float(end_animation_time) / end_animation_frames
            text.draw_string(self.surface, "GAME OVER", util.WHITE,
                             math.log(t + 0.001) * 150,
                             [self.width / 2, self.height / 2],
                             centre = True,
                             angle = 180)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def epilogue(self):
        while not self.quit and not self.any_key:
            self.scan_input()
            self.world.update()
            self.update_alien()

            self.surface.fill(util.BLACK)
            text.draw_string(self.surface, "ANY KEY TO PLAY AGAIN", 
                             util.WHITE,
                             20,
                             [self.width / 2, self.height / 2],
                             centre = True,
                             angle = 0)
            self.draw_hud()
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def play_game(self):
        self.start_screen()

        while not self.quit:
            self.level = 1
            self.world.reset()

            while not self.quit:
                self.level_start()

                if not self.player:
                    self.player = ship.Ship(self.world)
                for i in range(2 ** self.level):
                    asteroid.Asteroid(self.world, random.randint(75, 100))

                self.play_level()

                if self.player and self.player.kill:
                    self.player = None
                    break

                self.level += 1

            self.game_over()
            self.epilogue()

def main():
    pygame.init()

    font = pygame.font.Font(None, 16)

    surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    #surface = pygame.display.set_mode([640, 480])
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Argh, it's the Asteroids!!")

    game = Game(surface)

    game.play_game()

    pygame.quit()

if __name__ == "__main__":
    main()
