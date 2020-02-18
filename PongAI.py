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

def draw_window(win, rackets1, rackets2, ball, score, alive, gen, max_fitness):
    win.blit(BACKGROUND_IMG, (0, 0))
    ball.draw(win)

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

    ball = Ball(WIN_WIDTH/2, WIN_HEIGHT/2)
    ball.set_max_height(WIN_HEIGHT)
    ball.set_max_width(WIN_WIDTH)
    ball.prepare()

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
        colisions.append(0)

    while run:
        clock.tick(FPS)
        last_direction = ball.get_dx()
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


            output = nets[x].activate((rackets1[x].x, rackets1[x].y, rackets2[x].x, rackets2[x].y, ball.x, ball.y))

            if output[0] < 0.5:
                rackets1[x].moveDown()
            if output[1] >= 0.5:
                rackets1[x].moveUp()
            if output[2] < 0.5:
                rackets2[x].moveDown()
            if output[3] >= 0.5:
                rackets2[x].moveUp()
            
            if rackets1[x].collide(ball) or rackets2[x].collide(ball):
                ge[x].fitness += 5
                colisions[x] = 1
            else:
                colisions[x] = 0

            if ge[x].fitness > MAX_FITNESS:
                MAX_FITNESS = ge[x].fitness

            if ball.x < rackets1[x].x or ball.x > rackets2[x].x:    # lost
                    ge[x].fitness -= 1
                    rackets1.pop(x)
                    rackets2.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    colisions.pop(x)

        counter = 0
        delete = []
        for c in colisions:
            if c == 1:
                score += 1
                ball.change_direction()
                for i, c in enumerate(colisions):
                    if i != 1:
                        ge[counter].fitness -= 1
                        rackets1.pop(counter)
                        rackets2.pop(counter)
                        nets.pop(counter)
                        ge.pop(counter)
                        colisions.pop(counter)
                    counter += 1
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
        ball.move()
        draw_window(win, rackets1, rackets2, ball, score, len(rackets1), GEN, MAX_FITNESS)

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