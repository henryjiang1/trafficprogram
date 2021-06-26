import pygame
import random
from car import Car
from pygame.math import Vector2


class traffic_director:
    def __init__(self, top1, top2, top3, bottom1, bottom2, bottom3, left1, left2, right1, right2):
        self.top1 = top1
        self.bottom1 = bottom1
        self.left1 = left1
        self.right1 = right1
        self.top2 = top2
        self.bottom2 = bottom2
        self.left2 = left2
        self.right2 = right2
        self.top3 = top3
        self.bottom3 = bottom3

        self.arrays = {'top': [], 'bottom': [], 'left': [], 'right': []}
        self.array_state = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}

        self.light_state = 0

        self.front_cars = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}

        self.yellow_light_timer = 0
        self.yellow_light_state = False

        self.moving_cars = []

    def greenlight(self, val):
        self.light_state = val

    def yellowlight(self, val, cars):
        self.yellow_light_timer = 0

        self.moving_cars = []
        for car in cars:
            if car.intersection_collision and car.velocity == Vector2(150, 0):
                self.moving_cars.append(car)

        self.light_state_val = val
        self.yellow_light_state = True

    def update(self, cars):
        self.arrays = {'top': [], 'bottom': [], 'left': [], 'right': []}
        self.array_state = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}

        self.front_cars = {'top': [], 'bottom': [], 'left': [], 'right': []}

        front_car_vals = {'top': [], 'bottom': [], 'left': [], 'right': []}

        for car in cars:
            if car.angle == 0 and self.left1 < car.position.x < self.left2:
                self.arrays['left'].append(car)
            elif car.angle == 90 and car.position.y > self.bottom1 and self.bottom2 < car.position.x < self.bottom3:
                self.arrays['bottom'].append(car)
            elif car.angle == 180 and self.right1 < car.position.x < self.right2:
                self.arrays['right'].append(car)
            elif car.angle == 270 and car.position.y < self.top1 and self.top2 < car.position.x < self.top3:
                self.arrays['top'].append(car)

        for car in self.arrays['top']:
            front_car_vals['top'].append(car.position.x)
        for car in self.arrays['bottom']:
            front_car_vals['bottom'].append(car.position.x)
        for car in self.arrays['left']:
            front_car_vals['left'].append(car.position.x)
        for car in self.arrays['right']:
            front_car_vals['right'].append(car.position.x)

        if len(front_car_vals['top']) >= 1:
            top_max = max(front_car_vals['top'])
        else:
            top_max = 0
        if len(front_car_vals['bottom']) >= 1:
            bottom_min = min(front_car_vals['bottom'])
        else:
            bottom_min = 0
        if len(front_car_vals['left']) >= 1:
            left_max = max(front_car_vals['left'])
        else:
            left_max = 0
        if len(front_car_vals['right']) >= 1:
            right_min = min(front_car_vals['right'])
        else:
            right_min = 0

        for car in self.arrays['top']:
            if car.position.y == top_max:
                self.front_cars['top'].append(car)
        for car in self.arrays['bottom']:
            if car.position.y == bottom_min:
                self.front_cars['bottom'].append(car)
        for car in self.arrays['left']:
            if car.position.x == left_max:
                self.front_cars['left'].append(car)
        for car in self.arrays['right']:
            if car.position.x == right_min:
                self.front_cars['right'].append(car)

        # yellow light
        if self.yellow_light_state:
            self.light_state = 0
            for car in self.moving_cars:
                car.velocity = Vector2(150, 0)
            self.yellow_light_timer += 1

        if self.yellow_light_timer > 100:
            self.greenlight(self.light_state_val)
            self.yellow_light_state = False

        self.change_state(self.light_state)

    def one(self):
        self.array_state = {'top': 1, 'bottom': 1, 'left': 0, 'right': 0}

        for car in self.front_cars['top']:
            if car.turn_direction == 0:
                self.array_state['top'] = 0
                for car in self.arrays['top']:
                    if car != self.front_cars['top'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

        for car in self.front_cars['bottom']:
            if car.turn_direction == 0:
                self.array_state['bottom'] = 0
                for car in self.arrays['bottom']:
                    if car != self.front_cars['bottom'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

    def two(self):
        self.array_state = {'top': 0, 'bottom': 0, 'left': 1, 'right': 1}

        for car in self.front_cars['left']:
            if car.turn_direction == 0:
                self.array_state['left'] = 0
                for car in self.arrays['left']:
                    if car != self.front_cars['left'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

        for car in self.front_cars['right']:
            if car.turn_direction == 0:
                self.array_state['right'] = 0
                for car in self.arrays['right']:
                    if car != self.front_cars['right'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

    def three(self):
        self.array_state = {'top': 1, 'bottom': 1, 'left': 0, 'right': 0}

        for car in self.front_cars['top']:
            if car.turn_direction == 1 or car.turn_direction == 2:
                self.array_state['top'] = 0
                for car in self.arrays['top']:
                    if car != self.front_cars['top'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

        for car in self.front_cars['bottom']:
            if car.turn_direction == 1 or car.turn_direction == 2:
                self.array_state['bottom'] = 0
                for car in self.arrays['bottom']:
                    if car != self.front_cars['bottom'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

    def four(self):
        self.array_state = {'top': 0, 'bottom': 0, 'left': 1, 'right': 1}

        for car in self.front_cars['left']:
            if car.turn_direction == 1 or car.turn_direction == 2:
                self.array_state['left'] = 0
                for car in self.arrays['left']:
                    if car != self.front_cars['left'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

        for car in self.front_cars['right']:
            if car.turn_direction == 1 or car.turn_direction == 2:
                self.array_state['right'] = 0
                for car in self.arrays['right']:
                    if car != self.front_cars['right'][0] and car.intersection_collision:
                        car.velocity = Vector2(150, 0)

    def five(self):
        self.array_state = {'top': 0, 'bottom': 1, 'left': 0, 'right': 0}

    def six(self):
        self.array_state = {'top': 1, 'bottom': 0, 'left': 0, 'right': 0}

    def seven(self):
        self.array_state = {'top': 0, 'bottom': 0, 'left': 1, 'right': 0}

    def eight(self):
        self.array_state = {'top': 0, 'bottom': 0, 'left': 0, 'right': 1}

    def change_state(self, arg):
        switch = {0: self.one, 1: self.two, 2: self.three, 3: self.four, 4: self.five, 5: self.six, 6: self.seven, 7: self.eight}

        func = switch.get(arg, lambda: "Invalid state")
        return func()