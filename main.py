#!/usr/bin/python

import pygame
import random

import util
import ship
import asteroid
import alien
import sprite
import text

def main():
    pygame.init()

    font = pygame.font.Font(None, 16)

    surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    #surface = pygame.display.set_mode([640, 480])
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Argh, it's the Asteroids!!")

    world = sprite.World(surface)

    text.Character.string(world, 'ARGH ITS THE ASTEROIDS', 
                          [world.width / 2, 100], scale = 20)
    text.Character.string(world, 'PRESS ESC TO QUIT', 
                          [world.width / 2, 300], scale = 10)
    text.Character.string(world, 'PRESS LEFT AND RIGHT TO ROTATE', 
                          [world.width / 2, 400], scale = 10)
    text.Character.string(world, 'PRESS UP FOR THRUST', 
                          [world.width / 2, 500], scale = 10)
    text.Character.string(world, 'PRESS SPACE FOR FIRE', 
                          [world.width / 2, 600], scale = 10)
    text.Character.string(world, 'OR USE MOUSE CONTROLS', 
                          [world.width / 2, 700], scale = 10)
    text.Character.string(world, 'WATCH OUT FOR ALLEN THE ALIEN', 
                          [world.width / 2, 800], scale = 10)
    text.Character.string(world, 'ANY KEY TO START', 
                          [world.width / 2, 1000], scale = 20)

    for i in range(4):
        x = asteroid.Asteroid(world, random.randint(50, 100))
        x.position[0] = 0

    clock = pygame.time.Clock()
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
            alien.Alien(world)

        world.update()

        surface.fill(util.BLACK)

        world.draw()

        clock.tick(60)

        pygame.display.flip()

    world.remove_all()

    done = False
    clock = pygame.time.Clock()
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
        asteroid.Asteroid(world, random.randint(75, 100))

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
            alien.Alien(world)

        world.update()

        if world.n_asteroids == 0:
            level += 1
            for i in range(2 ** level):
                asteroid.Asteroid(world, random.randint(75, 100))
            player.kill = True
            player = None
            start_animation_time = start_animation_frames

        surface.fill(util.BLACK)

        text.draw_string(surface, "SCORE %d" % world.score, 
                         util.WHITE, 10, [10, 20])
        text.draw_string(surface, "LEVEL %d" % level, 
                         util.WHITE, 10, [10, 40])

        if info:
            text.draw_string(surface, "FPS %d" % clock.get_fps(),
                             util.WHITE, 5, [10, world.height - 20])
            text.draw_string(surface, "OBJECTS %d" % len(world.sprites),
                             util.WHITE, 5, [10, world.height - 30])

        if start_animation_time > 0:
            t = float(start_animation_time) / start_animation_frames
            text.draw_string(surface, "LEVEL START", util.WHITE,
                             t * 150,
                             [world.width / 2, world.height / 2],
                             centre = True, 
                             angle = t * 200.0)

            if spawn:
                asteroid.Asteroid(world, random.randint(50, 100))

            start_animation_time -= 1
            if start_animation_time == 0:
                player = ship.Ship(world)

        world.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
