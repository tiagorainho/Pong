import pygame
import os
import time
import neat
from Racket import Racket
from Ball import Ball

pygame.font.init()
BACKGROUND_IMG = pygame.image.load(os.path.join("images", "background.png"))
WIN_HEIGHT = BACKGROUND_IMG.get_height()
WIN_WIDTH = BACKGROUND_IMG.get_width()
FPS = 30
GEN = 0
TIME_BETWEEN_KEYS = 0.2
START_COUNTER_KEYS = 0.0
STAT_FONT = pygame.font.SysFont("comicsans", 50)
MAX_FITNESS = 0

def waitToStart():
    time.sleep(0.5)  

def get_racket(x):
    racket = Racket(x)
    racket.set_max_height(WIN_HEIGHT)
    return racket

def draw_window(win, rackets1, rackets2, balls, score, alive, gen, max_fitness):
    win.blit(BACKGROUND_IMG, (0, 0))

    text = STAT_FONT.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (WIN_WIDTH - 50 - text.get_width(), 10))

    text = STAT_FONT.render("Alive: " + str(alive), 1, (0,0,0))
    win.blit(text, (50, 10))

    text = STAT_FONT.render("GEN: " + str(gen), 1, (0,0,0))
    win.blit(text, (50, WIN_HEIGHT - text.get_height() - 10))

    max_fitness = "{0:.2f}".format(round(max_fitness, 2))
    text = STAT_FONT.render("max fit: " + str(max_fitness), 1, (0,0,0))
    win.blit(text, (WIN_WIDTH - 50 - text.get_width(), WIN_HEIGHT - text.get_height() - 10))

    for x in range(len(rackets1)):
        rackets1[x].draw(win)
        rackets2[x].draw(win)
        balls[x].draw(win)
    pygame.display.update()      

def main(genomes, config):
    global GEN
    global START_COUNTER_KEYS
    global FPS
    global MAX_FITNESS

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    last_score = -1
    score = 0
    run = True

    balls = []
    nets = []
    ge = []
    rackets1 = []
    rackets2 = []

    colisions = []

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        rackets1.append(Racket(20, WIN_HEIGHT/2))
        rackets2.append(Racket(WIN_WIDTH - 20, WIN_HEIGHT/2))
        g.fitness = 0
        ge.append(g)
        ball = Ball(WIN_WIDTH/2, WIN_HEIGHT/2)
        ball.set_max_height(WIN_HEIGHT)
        ball.set_max_width(WIN_WIDTH)
        ball.prepare()
        balls.append(ball)
        colisions.append(0)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        if not len(ge) > 0:
            run = False
            break
        for x, racket1 in enumerate(rackets1):
            
            ge[x].fitness += 0.1

            #output = nets[x].activate((rackets1[x].y, abs(rackets1[x].x - ball.x), abs(ball.y)))

            #output = nets[x].activate((rackets1[x].x, rackets1[x].y, rackets2[x].x, rackets2[x].y, balls[x].x, balls[x].y))

            #
            output = nets[x].activate((rackets1[x].y, rackets2[x].y, abs(rackets1[x].x - balls[x].x), abs(rackets1[x].y - balls[x].y), abs(rackets2[x].x - balls[x].x), abs(rackets2[x].y - balls[x].y)))
            '''
            if output[0] < 0.5:
                rackets1[x].moveDown()
            if output[1] >= 0.5:
                rackets1[x].moveUp()
            '''

            if output[0] < 0.5:
                rackets1[x].moveDown()
            if output[1] >= 0.5:
                rackets1[x].moveUp()
            if output[2] < 0.5:
                rackets2[x].moveDown()
            if output[3] >= 0.5:
                rackets2[x].moveUp()
            
            if rackets1[x].collide(balls[x]) or rackets2[x].collide(balls[x]):
                balls[x].change_direction()
                ge[x].fitness += 5
                colisions[x] = 1
            else:
                colisions[x] = 0

            if ge[x].fitness > MAX_FITNESS:
                MAX_FITNESS = ge[x].fitness

            balls[x].move()

            if balls[x].x < rackets1[x].x or balls[x].x > rackets2[x].x:    # lost
                    rackets1.pop(x)
                    rackets2.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    colisions.pop(x)
                    balls.pop(x)            

        for c in colisions:
            if c == 1:
                score += 1
                break

        pressed = pygame.key.get_pressed()
        if time.time() - START_COUNTER_KEYS > TIME_BETWEEN_KEYS:
            START_COUNTER_KEYS = time.time()
            if pressed[pygame.K_RIGHT]:
                if FPS < 60:
                    FPS = FPS * 2
                    print("Current fps: " + str(FPS))
                else:
                    print("Max velocity reached")
            if pressed[pygame.K_LEFT]:
                if FPS > 1:
                    FPS = FPS / 2
                    print("Current fps: " + str(FPS))
                else:
                    print("Min velocity reached")

        draw_window(win, rackets1, rackets2, balls, score, len(rackets1), GEN, MAX_FITNESS)

    GEN += 1


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(main, 50)



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "configAI.txt")
    run(config_path)