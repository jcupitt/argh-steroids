#!/usr/bin/python

import pygame
import random

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
        text.Character.string(self.world, 'ARGH ITS THE ASTEROIDS', 
                              [self.width / 2, 100], scale = 20)
        text.Character.string(self.world, 'PRESS ESC TO QUIT', 
                              [self.width / 2, 300], scale = 10)
        text.Character.string(self.world, 'PRESS LEFT AND RIGHT TO ROTATE', 
                              [self.width / 2, 400], scale = 10)
        text.Character.string(self.world, 'PRESS UP FOR THRUST', 
                              [self.width / 2, 500], scale = 10)
        text.Character.string(self.world, 'PRESS SPACE FOR FIRE', 
                              [self.width / 2, 600], scale = 10)
        text.Character.string(self.world, 'OR USE MOUSE CONTROLS', 
                              [self.width / 2, 700], scale = 10)
        text.Character.string(self.world, 'WATCH OUT FOR ALLEN THE ALIEN', 
                              [self.width / 2, 800], scale = 10)
        text.Character.string(self.world, 'ANY KEY TO START', 
                              [self.width / 2, 1000], scale = 20)

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

        self.world.remove_all()

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

        alien_time = random.randint(200, 400)

        level = 1

        player = None
        for i in range(2 ** level):
            asteroid.Asteroid(self.world, random.randint(75, 100))

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

            if self.world.n_asteroids == 0:
                level += 1
                for i in range(2 ** level):
                    asteroid.Asteroid(self.world, random.randint(75, 100))
                player.kill = True
                player = None
                start_animation_time = start_animation_frames

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
                t = float(start_animation_time) / start_animation_frames
                text.draw_string(self.surface, "LEVEL START", util.WHITE,
                                 t * 150,
                                 [self.width / 2, self.height / 2],
                                 centre = True, 
                                 angle = t * 200.0)

                if spawn:
                    asteroid.Asteroid(self.world, random.randint(50, 100))

                start_animation_time -= 1
                if start_animation_time == 0:
                    player = ship.Ship(self.world)

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
