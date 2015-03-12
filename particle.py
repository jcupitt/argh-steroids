
import random
import pygame

import util

# stolen from a PET scanner
colour_table = [[ 15, 0, 30 ],
                [ 19, 0, 40 ],
                [ 23, 0, 48 ],
                [ 28, 0, 57 ],
                [ 36, 0, 74 ],
                [ 42, 0, 84 ],
                [ 46, 0, 93 ],
                [ 51, 0, 102 ],
                [ 59, 0, 118 ],
                [ 65, 0, 130 ],
                [ 69, 0, 138 ],
                [ 72, 0, 146 ],
                [ 81, 0, 163 ],
                [ 47, 0, 95 ],
                [ 12, 0, 28 ],
                [ 64, 0, 144 ],
                [ 61, 0, 146 ],
                [ 55, 0, 140 ],
                [ 52, 0, 137 ],
                [ 47, 0, 132 ],
                [ 43, 0, 128 ],
                [ 38, 0, 123 ],
                [ 30, 0, 115 ],
                [ 26, 0, 111 ],
                [ 23, 0, 108 ],
                [ 17, 0, 102 ],
                [ 9, 0, 94 ],
                [ 6, 0, 91 ],
                [ 2, 0, 87 ],
                [ 0, 0, 88 ],
                [ 0, 0, 100 ],
                [ 0, 0, 104 ],
                [ 0, 0, 108 ],
                [ 0, 0, 113 ],
                [ 0, 0, 121 ],
                [ 0, 0, 125 ],
                [ 0, 0, 129 ],
                [ 0, 0, 133 ],
                [ 0, 0, 141 ],
                [ 0, 0, 146 ],
                [ 0, 0, 150 ],
                [ 0, 0, 155 ],
                [ 0, 0, 162 ],
                [ 0, 0, 167 ],
                [ 0, 0, 173 ],
                [ 0, 0, 180 ],
                [ 0, 0, 188 ],
                [ 0, 0, 193 ],
                [ 0, 0, 197 ],
                [ 0, 0, 201 ],
                [ 0, 0, 209 ],
                [ 0, 0, 214 ],
                [ 0, 0, 218 ],
                [ 0, 0, 222 ],
                [ 0, 0, 230 ],
                [ 0, 0, 235 ],
                [ 0, 0, 239 ],
                [ 0, 0, 243 ],
                [ 0, 0, 247 ],
                [ 0, 4, 251 ],
                [ 0, 10, 255 ],
                [ 0, 14, 255 ],
                [ 0, 18, 255 ],
                [ 0, 24, 255 ],
                [ 0, 31, 255 ],
                [ 0, 36, 255 ],
                [ 0, 39, 255 ],
                [ 0, 45, 255 ],
                [ 0, 53, 255 ],
                [ 0, 56, 255 ],
                [ 0, 60, 255 ],
                [ 0, 66, 255 ],
                [ 0, 74, 255 ],
                [ 0, 77, 255 ],
                [ 0, 81, 255 ],
                [ 0, 88, 251 ],
                [ 0, 99, 239 ],
                [ 0, 104, 234 ],
                [ 0, 108, 230 ],
                [ 0, 113, 225 ],
                [ 0, 120, 218 ],
                [ 0, 125, 213 ],
                [ 0, 128, 210 ],
                [ 0, 133, 205 ],
                [ 0, 141, 197 ],
                [ 0, 145, 193 ],
                [ 0, 150, 188 ],
                [ 0, 154, 184 ],
                [ 0, 162, 176 ],
                [ 0, 167, 172 ],
                [ 0, 172, 170 ],
                [ 0, 180, 170 ],
                [ 0, 188, 170 ],
                [ 0, 193, 170 ],
                [ 0, 197, 170 ],
                [ 0, 201, 170 ],
                [ 0, 205, 170 ],
                [ 0, 211, 170 ],
                [ 0, 218, 170 ],
                [ 0, 222, 170 ],
                [ 0, 226, 170 ],
                [ 0, 232, 170 ],
                [ 0, 239, 170 ],
                [ 0, 243, 170 ],
                [ 0, 247, 170 ],
                [ 0, 251, 161 ],
                [ 0, 255, 147 ],
                [ 0, 255, 139 ],
                [ 0, 255, 131 ],
                [ 0, 255, 120 ],
                [ 0, 255, 105 ],
                [ 0, 255, 97 ],
                [ 0, 255, 89 ],
                [ 0, 255, 78 ],
                [ 0, 255, 63 ],
                [ 0, 255, 55 ],
                [ 0, 255, 47 ],
                [ 0, 255, 37 ],
                [ 0, 255, 21 ],
                [ 0, 255, 13 ],
                [ 0, 255, 5 ],
                [ 2, 255, 2 ],
                [ 13, 255, 13 ],
                [ 18, 255, 18 ],
                [ 23, 255, 23 ],
                [ 27, 255, 27 ],
                [ 35, 255, 35 ],
                [ 40, 255, 40 ],
                [ 43, 255, 43 ],
                [ 48, 255, 48 ],
                [ 55, 255, 55 ],
                [ 60, 255, 60 ],
                [ 64, 255, 64 ],
                [ 69, 255, 69 ],
                [ 72, 255, 72 ],
                [ 79, 255, 79 ],
                [ 90, 255, 82 ],
                [ 106, 255, 74 ],
                [ 113, 255, 70 ],
                [ 126, 255, 63 ],
                [ 140, 255, 56 ],
                [ 147, 255, 53 ],
                [ 155, 255, 48 ],
                [ 168, 255, 42 ],
                [ 181, 255, 36 ],
                [ 189, 255, 31 ],
                [ 197, 255, 27 ],
                [ 209, 255, 21 ],
                [ 224, 255, 14 ],
                [ 231, 255, 10 ],
                [ 239, 255, 7 ],
                [ 247, 251, 3 ],
                [ 255, 243, 0 ],
                [ 255, 239, 0 ],
                [ 255, 235, 0 ],
                [ 255, 230, 0 ],
                [ 255, 222, 0 ],
                [ 255, 218, 0 ],
                [ 255, 214, 0 ],
                [ 255, 209, 0 ],
                [ 255, 201, 0 ],
                [ 255, 197, 0 ],
                [ 255, 193, 0 ],
                [ 255, 188, 0 ],
                [ 255, 180, 0 ],
                [ 255, 176, 0 ],
                [ 255, 172, 0 ],
                [ 255, 167, 0 ],
                [ 255, 156, 0 ],
                [ 255, 150, 0 ],
                [ 255, 146, 0 ],
                [ 255, 142, 0 ],
                [ 255, 138, 0 ],
                [ 255, 131, 0 ],
                [ 255, 125, 0 ],
                [ 255, 121, 0 ],
                [ 255, 117, 0 ],
                [ 255, 110, 0 ],
                [ 255, 104, 0 ],
                [ 255, 100, 0 ],
                [ 255, 96, 0 ],
                [ 255, 90, 0 ],
                [ 255, 83, 0 ],
                [ 255, 78, 0 ],
                [ 255, 75, 0 ],
                [ 255, 71, 0 ],
                [ 255, 67, 0 ],
                [ 255, 65, 0 ],
                [ 255, 63, 0 ],
                [ 255, 59, 0 ],
                [ 255, 54, 0 ],
                [ 255, 52, 0 ],
                [ 255, 50, 0 ],
                [ 255, 46, 0 ],
                [ 255, 41, 0 ],
                [ 255, 39, 0 ],
                [ 255, 36, 0 ],
                [ 255, 32, 0 ],
                [ 255, 25, 0 ],
                [ 255, 22, 0 ],
                [ 255, 20, 0 ],
                [ 255, 17, 0 ],
                [ 255, 13, 0 ],
                [ 255, 10, 0 ],
                [ 255, 7, 0 ],
                [ 255, 4, 0 ],
                [ 255, 0, 0 ],
                [ 252, 0, 0 ],
                [ 251, 0, 0 ],
                [ 249, 0, 0 ],
                [ 248, 0, 0 ],
                [ 244, 0, 0 ],
                [ 242, 0, 0 ],
                [ 240, 0, 0 ],
                [ 237, 0, 0 ],
                [ 234, 0, 0 ],
                [ 231, 0, 0 ],
                [ 229, 0, 0 ],
                [ 228, 0, 0 ],
                [ 225, 0, 0 ],
                [ 222, 0, 0 ],
                [ 221, 0, 0 ],
                [ 219, 0, 0 ],
                [ 216, 0, 0 ],
                [ 213, 0, 0 ],
                [ 212, 0, 0 ],
                [ 210, 0, 0 ],
                [ 207, 0, 0 ],
                [ 204, 0, 0 ],
                [ 201, 0, 0 ],
                [ 199, 0, 0 ],
                [ 196, 0, 0 ],
                [ 193, 0, 0 ],
                [ 192, 0, 0 ],
                [ 190, 0, 0 ],
                [ 188, 0, 0 ],
                [ 184, 0, 0 ],
                [ 183, 0, 0 ],
                [ 181, 0, 0 ],
                [ 179, 0, 0 ],
                [ 175, 0, 0 ]]
n_colour = len(colour_table)

class Particle(object):
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

        self.show_particles = True

        # a row of this hash stores:
        #
        # 0 - life .. down counter until death
        # 1 - x
        # 2 - y
        # 3 - u  horizontal component of velocity
        # 4 - v  vertical component of velocity
        # 5 - colour index ... int index into colour array above
        # 6 - colour delta ... add this to index each update
        self.particles = {}
        self.index = 0

    def show(self, show_particles):
        self.show_particles = show_particles

    def add(self, position, velocity, colour, colour_delta, life):
        if not self.show_particles:
            return

        particle = [life,
                    position[0], position[1], 
                    velocity[0], velocity[1],
                    colour, colour_delta]
        self.particles[self.index] = particle
        self.index += 1

    def n_particles(self):
        return len(self.particles)

    def remove_all(self):
        self.particles = {}

    def explosion(self, n_points, position, velocity):
        for i in range(n_points):
            delta = 360 / n_points
            angle = i * delta + random.randint(-delta / 2, delta / 2)
            speed = random.random() * 2.0 
            self.add(position, 
                     [velocity[0] + speed * util.cos(angle),
                      velocity[1] + speed * util.sin(angle)],
                     n_colour - random.randint(1, 50), 
                     -1, 
                     random.randint(50, 100))

    def explosion2(self, n_points, position, velocity):
        for i in range(n_points):
            delta = 360.0 / n_points
            angle = i * delta + random.randint(int(-delta), int(delta))
            speed = random.random() * 4.0 
            self.add(position, 
                     [velocity[0] + speed * util.cos(angle),
                      velocity[1] + speed * util.sin(angle)],
                     n_colour - random.randint(1, 50), 
                     -1, 
                     random.randint(50, 400))

    def sparks(self, position, velocity):
        n_points = 3
        delta = 360 / n_points
        for i in range(n_points):
            angle = i * delta + random.randint(-delta / 2, delta / 2)
            speed = random.random() * 2.0 
            self.add(position, 
                     [velocity[0] + speed * util.cos(angle),
                      velocity[1] + speed * util.sin(angle)],
                     n_colour - random.randint(1, 200), 
                     -113, 
                     random.randint(50, 100))

    def jet(self, position, velocity, angle):
        angle = angle + random.randint(-10, 10) + 180
        u = 2 * util.cos(angle)
        v = 2 * util.sin(angle)
        self.add([position[0] + 3 * u, position[1] + 3 * v],
                 [velocity[0] + u, velocity[1] + v],
                 random.randint(50, 200),
                 random.randint(5, 10),
                 random.randint(20, 30))

    def starfield(self):
        for i in range(50):
            self.add([random.randint(0, self.width),
                      random.randint(0, self.height)],
                     [0, 0],
                     random.randint(50, 200),
                     random.randint(1, 3),
                     100000000)

    def update(self):
        if not self.show_particles:
            return

        keys = self.particles.keys()
        for i in keys:
            part = self.particles[i]
            if part[0] > 0:
                part[0] -= 1
                if part[0] == 0:
                    del self.particles[i]
                    continue

                part[1] += part[3]
                part[2] += part[4]
                part[1] %= self.width
                part[2] %= self.height

                part[5] += part[6]
                part[5] %= n_colour

    def draw(self):
        if not self.show_particles:
            return

        for i in self.particles:
            part = self.particles[i]
            rect = [part[1], part[2], 3, 3]
            pygame.draw.rect(self.surface, colour_table[part[5]], rect)

