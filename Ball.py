import pygame
import os
import random
import math

class Ball:

    BALL_IMG = pygame.image.load(os.path.join("images", "ball2.png"))
    OFFSET = 10
    START_VELOCITY = 10

    def __init__(self, x, y):
        self.initial_x = x
        self.initial_y = y
        self.set_initial_location()
        self.velocity = self.START_VELOCITY
        self.direction = 0
        self.max_height = 0
        self.max_width = 0
        self.middle_x = x

    def get_dx(self):
        return self.x - self.last_position[0]

    def get_dy(self):
        return self.y - self.last_position[1]

    def get_dy_with_velocity(self, dx):
        return math.sqrt(self.velocity**2 - dx**2) #round(math.sqrt(vel**2 - dx**2))

    def set_initial_location(self):
        self.velocity = self.START_VELOCITY
        self.x = self.initial_x
        self.y = self.initial_y
        self.last_position = (self.x, self.y)

    def increase_speed(self, value):
        pass

    def prepare(self):
        self.set_initial_location()
        self.x += random.randint(self.velocity - 2, self.velocity) * random.choice([-1, 1])
        self.y += self.get_dy_with_velocity(self.get_dx()) * random.choice([-1, 1])
        self.velocity = self.START_VELOCITY

    def change_direction(self):
        temp = [self.x, self.y]
        self.x = self.last_position[0]
        self.y = self.last_position[1]

        if self.y < temp[1]:
            self.y += 5
        elif self.y > temp[1]:
            self.y -= 5
        else:
            self.y += random.randrange(-5, 5)
        self.last_position = temp

    def move(self):
        temp = [self.x, self.y]
        if self.colide_with_field():
            self.y -= self.get_dy()
        else:
            self.y += self.get_dy()

        self.x += self.get_dx()
        self.last_position = temp
        

    def get_mask(self):
        return pygame.mask.from_surface(self.BALL_IMG)

    def draw(self, win):
        win.blit(self.BALL_IMG, (self.x, self.y))

    def set_max_height(self, y):
        self.max_height = y - self.BALL_IMG.get_height()

    def set_max_width(self, x):
        self.max_width = x
    
    def colide_with_field(self):
        if self.y >= self.max_height or self.y <= 0:
            return True
        return False

    def racket_successful(self, racket):
        if racket.x < self.middle_x:
            if self.x < racket.x:
                return False
        else:
            if self.x > racket.x:
                return False
        return True


    def hasWinner(self):
        if self.x >= self.max_width or self.x <= 0:
            return True
        return False