import pygame
import os

class Racket:
    RACKET_IMG = pygame.image.load(os.path.join("images", "racket6.png"))
    DISPLACEMENT = 10
    RISK_HEIGHT = 10

    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.max_height = 0

    def moveUp(self):
        if self.y - self.RISK_HEIGHT > 0:
            self.y -= self.DISPLACEMENT
        
    def moveDown(self):
        if self.y < self.max_height:
            self.y += self.DISPLACEMENT

    def draw(self, win):
        win.blit(self.RACKET_IMG, (self.x, self.y))

    def set_max_height(self, y):
        self.max_height = y - self.RISK_HEIGHT - self.RACKET_IMG.get_height()
    

    def get_mask(self):
        return pygame.mask.from_surface(self.RACKET_IMG)

    def collide(self, ball):
        racket_mask = pygame.mask.from_surface(self.RACKET_IMG)
        ball_mask = ball.get_mask()

        offset = (round(ball.x - self.x), round(ball.y - self.y))
        
        if racket_mask.overlap(ball_mask, offset):
            return True
        return False