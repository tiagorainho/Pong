import pygame
import os
import time
from Racket import Racket
from Ball import Ball

BACKGROUND_IMG = pygame.image.load(os.path.join("images", "background.png"))
WIN_HEIGHT = BACKGROUND_IMG.get_height()
WIN_WIDTH = BACKGROUND_IMG.get_width()
FPS = 30

def get_racket(x):
    racket = Racket(x)
    racket.set_max_height(WIN_HEIGHT)
    return racket

def draw_window(win, racket1, racket2, ball):
    win.blit(BACKGROUND_IMG, (0, 0))
    ball.draw(win)
    racket1.draw(win)
    racket2.draw(win)
    pygame.display.update()

def waitToStart():
    time.sleep(0.5)        

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    racket2 = get_racket(20)
    racket1 = get_racket(WIN_WIDTH - 20)
    clock = pygame.time.Clock()
    run = True

    ball = Ball(WIN_WIDTH/2, WIN_HEIGHT/2)
    ball.set_max_height(WIN_HEIGHT)
    ball.set_max_width(WIN_WIDTH)
    ball.prepare()

    last_score = -1
    score = 0

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if racket1.collide(ball) or racket2.collide(ball):
            score += 1
            ball.change_direction()

        if ball.hasWinner():
            ball.prepare()
            waitToStart()
        ball.move()

        pressed1 = pygame.key.get_pressed()
        pressed2 = pygame.key.get_pressed()
        if pressed1[pygame.K_UP]:
            racket1.moveUp()
        elif pressed1[pygame.K_DOWN]:
            racket1.moveDown()
        if pressed2[pygame.K_w]:
            racket2.moveUp()
        elif pressed2[pygame.K_s]:
            racket2.moveDown()

        #if score > last_score:
        #    ball.increase_speed(1.1)

        last_score = score
        draw_window(win, racket1, racket2, ball)

if __name__ == "__main__":
    main()