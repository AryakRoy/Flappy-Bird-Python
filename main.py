import pygame as pg
import random
import sys
import time
from pygame.locals import *

FPS = 40
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

GAME_SPRITES = {}
GAME_SPRITES['message'] = pg.image.load('gallery/sprites/message.png').convert_alpha()
GAME_SPRITES['background'] = pg.image.load('gallery/sprites/background.png').convert_alpha()
GAME_SPRITES['base'] = pg.image.load('gallery/sprites/base.png').convert_alpha()
GAME_SPRITES['player'] = pg.image.load('gallery/sprites/bird.png').convert_alpha()
GAME_SPRITES['pipe'] = (pg.transform.rotate(pg.image.load('gallery/sprites/pipe.png'),180),pg.image.load('gallery/sprites/pipe.png'))
GAME_SPRITES['game_over'] = pg.image.load('gallery/sprites/game-over.png').convert_alpha()
GAME_SPRITES['score'] = pg.image.load('gallery/sprites/score.png').convert_alpha()



ground_y = SCREEN_HEIGHT * 0.8
base_x = 0
pg.init()
FPSCLOCK = pg.time.Clock()
pg.display.set_caption('Flappy Bird')
icon = pg.image.load('gallery/sprites/icon.png')
pg.display.set_icon(icon)
SOUNDS ={}
SOUNDS['wing'] = pg.mixer.Sound('sounds/sfx_wing.wav')
SOUNDS['point'] = pg.mixer.Sound('sounds/sfx_point.wav')
SOUNDS['hit'] = pg.mixer.Sound('sounds/sfx_hit.wav')
SOUNDS['die'] = pg.mixer.Sound('sounds/sfx_die.wav')

NUMBERS = {
    '0':pg.image.load('gallery/sprites/0.png').convert_alpha(),
    '1':pg.image.load('gallery/sprites/1.png').convert_alpha(),
    '2':pg.image.load('gallery/sprites/2.png').convert_alpha(),
    '3':pg.image.load('gallery/sprites/3.png').convert_alpha(),
    '4':pg.image.load('gallery/sprites/4.png').convert_alpha(),
    '5':pg.image.load('gallery/sprites/5.png').convert_alpha(),
    '6':pg.image.load('gallery/sprites/6.png').convert_alpha(),
    '7':pg.image.load('gallery/sprites/7.png').convert_alpha(),
    '8':pg.image.load('gallery/sprites/8.png').convert_alpha(),
    '9':pg.image.load('gallery/sprites/9.png').convert_alpha(),
}

def welcome_screen():
    player_x = int(SCREEN_WIDTH/5)
    player_y = int((SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2)
    message_x = int((SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2)
    message_y = int(SCREEN_HEIGHT*0.13)
    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(player_x,player_y))
                SCREEN.blit(GAME_SPRITES['message'],(message_x,message_y))
                SCREEN.blit(GAME_SPRITES['base'],(base_x,ground_y))
                pg.display.update()
                FPSCLOCK.tick(FPS)
def game_over(SCORE):
    pg.mixer.Sound.play(SOUNDS['die'])
    while True:
        game_x = int(SCREEN_WIDTH - GAME_SPRITES['game_over'].get_width())/2
        game_y = int(SCREEN_HEIGHT/5)
        score_x = int(SCREEN_WIDTH - GAME_SPRITES['score'].get_width())/2
        score_y = int(SCREEN_HEIGHT/2) - 50
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['base'],(base_x,ground_y))
                SCREEN.blit(GAME_SPRITES['game_over'],(game_x,game_y))
                SCREEN.blit(GAME_SPRITES['score'],(score_x,score_y))
                score = str(SCORE)
                indent = 0
                for s in score:
                    SCREEN.blit(NUMBERS[s],((SCREEN_WIDTH - NUMBERS[s].get_height())/2 + indent,SCREEN_HEIGHT - GAME_SPRITES['base'].get_height() - 100))
                    indent += 25
                pg.display.update()
                FPSCLOCK.tick(FPS)
def get_random_pipe():
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    fixpoint = int(SCREEN_HEIGHT/3)
    y2=random.randint(int(fixpoint+0.2*fixpoint),int(SCREEN_HEIGHT-GAME_SPRITES['base'].get_height()-0.5*fixpoint))
    y1=pipe_height-y2+100
    pipex=SCREEN_WIDTH+10
    pipe=[
        {'x':pipex,'y':-y1},#Upper Pipe
        {'x':pipex,'y':y2}#lowepipe
    ]
    return pipe

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> ground_y - 25  or playery<0:
        
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            
            return True
    return False
def isPass(playerx,upperPipes):
    x = playerx + int(GAME_SPRITES['player'].get_width()/2)
    for pipe in upperPipes:
        pipe_x = pipe['x'] + int(GAME_SPRITES['pipe'][0].get_width()/2)
        if abs(x - pipe_x) <2.5:
            return True
    return False

def main_game():
    player_x = int(SCREEN_WIDTH/5)
    player_y = int(SCREEN_HEIGHT/2)
    pipe_vel_x = -4
    player_vel_y = -8
    player_max_vel_y = 10
    player_min_vel_y = -8
    player_acc_y = 1
    player_flap_vel = -8
    newPipe1 = get_random_pipe()
    newPipe2 = get_random_pipe()
    upperPipes = [
        {'x': SCREEN_WIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y':newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREEN_WIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y':newPipe2[1]['y']},
    ]
    SCORE = 0
    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                pg.mixer.Sound.play(SOUNDS['wing'])
                if player_y > 0:
                    player_vel_y = player_flap_vel
        if player_vel_y < player_max_vel_y:
            player_vel_y +=player_acc_y

        player_height = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(player_vel_y,ground_y - player_y - player_height)

        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipe_vel_x
            lowerPipe['x'] += pipe_vel_x
        
        if 0<upperPipes[0]['x']<5:
           newpipe = get_random_pipe()
           upperPipes.append(newpipe[0])
           lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        crashTest=isCollide(player_x, player_y, upperPipes, lowerPipes)
        if crashTest:
            pg.mixer.Sound.play(SOUNDS['hit'])
            time.sleep(1)
            return SCORE

        passTest = isPass(player_x,upperPipes)
        if passTest:
            pg.mixer.Sound.play(SOUNDS['point'])
            SCORE = SCORE + 1

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        score = str(SCORE)
        indent = 0
        for s in score:
            SCREEN.blit(NUMBERS[s],((SCREEN_WIDTH - NUMBERS[s].get_height())/2 + indent,SCREEN_HEIGHT/15))
            indent += 25
        SCREEN.blit(GAME_SPRITES['player'],(player_x,player_y))
        SCREEN.blit(GAME_SPRITES['base'],(base_x,ground_y))
        pg.display.update()
        FPSCLOCK.tick(FPS)

while True:
    welcome_screen()
    s = main_game()
    game_over(s)