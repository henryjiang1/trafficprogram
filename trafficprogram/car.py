import pygame
import numpy as np
import random
from pygame.math import Vector2

carImg = pygame.image.load('car.png')
carImg = pygame.transform.scale(carImg, (92, 46))

RED = (230, 30, 30)


class Car:
    def __init__(self, screen, current_time):
        self.screen = screen
        self.carImg = carImg

        self.current_time = current_time
        self.respawn_time = self.current_time
        self.stopped_time = 0

        self.hitbox = (0, 0, 92, 72)
        self.front_hitbox = (0, 0, 23, 72)
        self.collision = False
        self.intersection_collision = False
        self.angle = 0
        self.turned = False

        self.turn_direction = 0
        self.location = 0
        self.arrived_at_destination = False

        self.respawn()

    def update(self, dt):
        # movement
        self.position += self.velocity.rotate(-self.angle) * dt

        # draw car
        rotated = pygame.transform.rotate(self.carImg, self.angle)
        rect = rotated.get_rect()
        self.screen.blit(rotated, self.position - (rect.width / 2, rect.height / 2))

        # turn
        self.get_turn_state()
        self.turning()

        # hitbox
        if self.angle == 0:
            self.hitbox = (self.position.x - 46, self.position.y - 36, 92, 72)
            self.front_hitbox = (self.position.x + 23, self.position.y - 36, 23, 72)
        elif self.angle == 90:
            self.hitbox = (self.position.x - 36, self.position.y - 46, 72, 92)
            self.front_hitbox = (self.position.x - 36, self.position.y - 46, 72, 23)
        elif self.angle == 180:
            self.hitbox = (self.position.x - 46, self.position.y - 36, 92, 72)
            self.front_hitbox = (self.position.x - 46, self.position.y - 36, 23, 72)
        elif self.angle == 270:
            self.hitbox = (self.position.x - 36, self.position.y - 46, 72, 92)
            self.front_hitbox = (self.position.x - 36, self.position.y + 23, 72, 23)

        pygame.draw.rect(self.screen, RED, self.hitbox, 1)
        # pygame.draw.rect(self.screen, RED, self.front_hitbox, 1)

        # on collision
        if self.collision:
            self.velocity = Vector2(0.0, 0.0)
        else:
            self.velocity = Vector2(150.0, 0.0)

        # reach destination
        if self.hitbox[0] < self.destination.x < self.hitbox[0] + self.hitbox[2]:
            if self.hitbox[1] < self.destination.y < self.hitbox[1] + self.hitbox[3]:
                #self.respawn()
                self.velocity = Vector2(0,0)
                self.arrived_at_destination = True
                self.hitbox = (0,0,0,0)
                self.stopped_time = 0
                self.turned = False

    def remove_destinations(self, destination_x, destination_y, high, low, angle):
        self.angle = angle
        for x in range(high, low - 1, -1):
            destination_x.pop(x)
            destination_y.pop(x)

    def respawn(self):
        spawn_x_vals = [50, 150, 250, 388, 388, 460, 460, 550, 650, 750, 850, 950, 550, 650, 750, 850, 950, 1060, 1060,
                        1132, 1132, 1250, 1350, 1450]
        spawn_y_vals = [348, 348, 348, 50, 150, 450, 550, 276, 276, 276, 276, 276, 348, 348, 348, 348, 348, 50, 150,
                        450, 550, 276, 276, 276]

        destination_x = [0, 388, 460, 1060, 1132, 1520]
        destination_y = [276, 624, 0, 624, 0, 348]

        # set position
        i = random.randint(0, 23)
        self.position = Vector2(spawn_x_vals[i], spawn_y_vals[i])
        if i <= 2:
            self.remove_destinations(destination_x, destination_y, 0, 0, 0)

        elif i == 3 or i == 4:
            self.remove_destinations(destination_x, destination_y, 2, 2, 270)

        elif i == 5 or i == 6:
            self.remove_destinations(destination_x, destination_y, 1, 1, 90)

        elif 7 <= i <= 11:
            self.remove_destinations(destination_x, destination_y, 5, 3, 180)

        elif 12 <= i <= 16:
            self.remove_destinations(destination_x, destination_y, 2, 0, 0)

        elif i == 17 or i == 18:
            self.remove_destinations(destination_x, destination_y, 4, 4, 270)

        elif i == 19 or i == 20:
            self.remove_destinations(destination_x, destination_y, 3, 3, 90)

        elif i >= 21:
            self.remove_destinations(destination_x, destination_y, 5, 5, 180)

        self.velocity = Vector2(150.0, 0.0)
        self.stopped_time = 0

        # set destination
        r = random.randrange(0, len(destination_x), 1)
        self.destination = Vector2(destination_x[r], destination_y[r])

        # set respawn timer
        self.respawn_timer = self.current_time

    def set_direction(self, a, b, c, d, v1, v2):
        self.location = a
        if self.destination == v1:
            self.turn_direction = b
        elif self.destination == v2:
            self.turn_direction = c
        else:
            self.turn_direction = d

    def get_turn_state(self):
        if self.position.x < 352 and self.angle == 0:
            self.set_direction(1, 2, 0, 1, Vector2(388, 624), Vector2(460, 0))

        elif 352 < self.position.x < 496 and 0 < self.position.y < 240 and self.angle == 270:
            self.set_direction(2, 2, 1, 0, Vector2(0, 276), Vector2(388, 624))

        elif 352 < self.position.x < 496 and 384 < self.position.y < 624 and self.angle == 90:
            self.set_direction(3, 0, 1, 2, Vector2(0, 276), Vector2(460, 0))

        elif 496 < self.position.x < 1024 and self.angle == 180:
            self.set_direction(4, 0, 2, 1, Vector2(388, 624), Vector2(460, 0))

        elif 496 < self.position.x < 1024 and self.angle == 0:
            self.set_direction(4, 2, 0, 1, Vector2(1060, 624), Vector2(1132, 0))

        elif 1024 < self.position.x < 1168 and 0 < self.position.y < 240 and self.angle == 270:
            self.set_direction(5, 0, 1, 2, Vector2(1520, 348), Vector2(1060, 624))

        elif 1024 < self.position.x < 1168 and 384 < self.position.y < 624 and self.angle == 90:
            self.set_direction(6, 2, 1, 0, Vector2(1520, 348), Vector2(1132, 0))

        elif self.position.x > 1168 and self.angle == 180:
            self.set_direction(7, 2, 0, 1, Vector2(1132, 0), Vector2(1060, 624))

    def turn_x(self, x1, x2, angle1, angle2):
        if self.turn_direction == 0 and x1 - 5 < self.position.x < x1 + 5:
            self.position.x = x1
            self.angle = angle1
            # self.turned = True
        elif self.turn_direction == 2 and x2 - 5 < self.position.x < x2 + 5:
            self.position.x = x2
            self.angle = angle2
            # self.turned = True
        else:
            pass

    def turn_y(self, y1, y2, angle1, angle2):
        if self.turn_direction == 0 and y1 - 5 < self.position.y < y1 + 5:
            self.position.y = y1
            self.angle = angle1
            # self.turned = True
        elif self.turn_direction == 2 and y2 - 5 < self.position.y < y2 + 5:
            self.position.y = y2
            self.angle = angle2
            # self.turned = True
        else:
            pass

    def turning(self):
        if self.location == 1 and self.angle == 0:
            self.turn_x(460, 388, 90, 270)

        elif self.location == 2 and self.angle == 270:
            self.turn_y(348, 276, 0, 180)

        elif self.location == 3 and self.angle == 90:
            self.turn_y(276, 348, 180, 0)

        elif self.location == 4 and self.angle == 180:
            self.turn_x(388, 460, 270, 90)

        elif self.location == 4 and self.angle == 0:
            self.turn_x(1132, 1060, 90, 270)

        elif self.location == 5 and self.angle == 270:
            self.turn_y(348, 276, 0, 180)

        elif self.location == 6 and self.angle == 90:
            self.turn_y(276, 348, 180, 0)

        elif self.location == 7 and self.angle == 180:
            self.turn_x(1060, 1132, 270, 90)
