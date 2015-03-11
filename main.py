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

        done = False
        alien_time = random.randint(200, 400)

        while not done:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True 

                if event.type == pygame.KEYDOWN :
                    done = True

            alien_time -= 1
            if alien_time < 0:
                alien_time = random.randint(1000, 2000)
                alien.Alien(self.world)

            self.world.update()

            self.surface.fill(util.BLACK)

            self.world.draw()

            self.clock.tick(60)

            pygame.display.flip()

        self.world.reset()

    def play(self):
        done = False
        rotate_left = False
        rotate_right = False
        thrust = False
        info = False
        fire = False
        spawn = False

        start_animation_frames = 100
        start_animation_time = start_animation_frames
        end_animation_frames = 100
        end_animation_time = 0
        waiting_for_keypress = False

        alien_time = random.randint(200, 400)

        level = 1

        player = None

        while not done:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True 

                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        done = event.type == pygame.KEYDOWN
                    elif event.key == pygame.K_LEFT:
                        rotate_left = event.type == pygame.KEYDOWN
                    elif event.key == pygame.K_RIGHT:
                        rotate_right = event.type == pygame.KEYDOWN
                    elif event.key == pygame.K_UP:
                        thrust = event.type == pygame.KEYDOWN
                    elif event.key == pygame.K_SPACE:
                        fire = event.type == pygame.KEYDOWN
                    elif event.key == pygame.K_s:
                        spawn = event.type == pygame.KEYDOWN
                    elif event.key == pygame.K_i:
                        info = event.type == pygame.KEYDOWN

                    if waiting_for_keypress:
                        waiting_for_keypress = False
                        start_animation_time = start_animation_frames
                        level = 1
                        self.world.reset()

                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        thrust = event.type == pygame.MOUSEBUTTONDOWN
                    elif event.button == 1:
                        fire = event.type == pygame.MOUSEBUTTONDOWN

            if player:
                if rotate_left:
                    player.rotate_left();
                if rotate_right:
                    player.rotate_right();
                if thrust:
                    player.thrust();
                if fire:
                    player.fire();

                x, y = pygame.mouse.get_rel()
                player.rotate_by(x / 5.0);

            alien_time -= 1
            if alien_time < 0:
                alien_time = random.randint(1000, 2000)
                alien.Alien(self.world)

            self.world.update()

            if self.world.n_asteroids == 0 and start_animation_time == 0:
                level += 1
                start_animation_time = start_animation_frames

            if player and player.kill:
                player = None
                end_animation_time = end_animation_frames

            self.surface.fill(util.BLACK)

            text.draw_string(self.surface, "SCORE %d" % self.world.score, 
                             util.WHITE, 10, [10, 20])
            text.draw_string(self.surface, "LEVEL %d" % level, 
                             util.WHITE, 10, [10, 40])

            if info:
                text.draw_string(self.surface, 
                                 "FPS %d" % self.clock.get_fps(),
                                 util.WHITE, 5, [10, self.height - 20])
                n_particles = self.world.particle.n_particles()
                n_sprites = len(self.world.sprites)
                text.draw_string(self.surface, 
                                 "OBJECTS %d" % (n_particles + n_sprites),
                                 util.WHITE, 5, [10, self.height - 30])

            if start_animation_time > 0:
                start_animation_time -= 1
                if start_animation_time == 0:
                    if not player:
                        player = ship.Ship(self.world)
                    for i in range(2 ** level):
                        asteroid.Asteroid(self.world, random.randint(75, 100))

                if spawn:
                    asteroid.Asteroid(self.world, random.randint(50, 100))

                t = float(start_animation_time) / start_animation_frames
                text.draw_string(self.surface, "LEVEL START", util.WHITE,
                                 t * 150,
                                 [self.width / 2, self.height / 2],
                                 centre = True, 
                                 angle = t * 200.0)

            if end_animation_time > 0:
                end_animation_time -= 1
                if end_animation_time == 0:
                    waiting_for_keypress = True

                t = float(end_animation_time) / end_animation_frames
                text.draw_string(self.surface, "GAME OVER", util.WHITE,
                                 math.log(t + 0.001) * 150,
                                 [self.width / 2, self.height / 2],
                                 centre = True,
                                 angle = 180)

            if waiting_for_keypress:
                text.draw_string(self.surface, "ANY KEY TO PLAY AGAIN", 
                                 util.WHITE,
                                 20,
                                 [self.width / 2, self.height / 2],
                                 centre = True,
                                 angle = 0)

            self.world.draw()

            self.clock.tick(60)

            pygame.display.flip()

def main():
    pygame.init()

    font = pygame.font.Font(None, 16)

    surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    #surface = pygame.display.set_mode([640, 480])
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Argh, it's the Asteroids!!")

    game = Game(surface)

    game.start_screen()

    game.play()

    pygame.quit()

if __name__ == "__main__":
    main()
