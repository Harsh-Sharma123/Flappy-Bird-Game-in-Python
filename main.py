import pygame
import sys  # to use sys.exit() to exit the program
from pygame.locals import *   # Basic pygame imports
import random     # for generating random numbers

# Global Variables
FPS = 40           # frames per second
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUND = {}
PLAYER = 'sprites/bird.png'
BACKGROUND = 'sprites/background.png'
PIPE = 'sprites/pipe.png'

def welcomeScreen():
    """
    shows welcome screen on the screen
    """
    playerx = int(SCREENWIDTH/2)
    playery = int(SCREENWIDTH - GAME_SPRITES['player'].get_height())/2
    messagex = int(SCREENWIDTH - GAME_SPRITES['message'].get_width())/2
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # if the user presses space or up key then the game starts
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
                
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top roatated) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},   # for upper pipe
        {'x': pipex, 'y': y2}     # for lower pipe
    ]
    return pipe

def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - 25  or playery < 0:
        GAME_SOUND['hit'].play()
        return True
    
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND ['hit'].play()
            return True

    for pipe in lowerpipes: 
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUND['hit'].play()
            return True 
    return False
     
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    # my list of upper pipes
    upperpipes = [
        {'x': SCREENWIDTH+200, 'y': newpipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newpipe2[0]['y']}
    ]
    # my list of lower pipes
    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8             # velocity while flapping
    playerFlapped = False           # it is true only when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUND['wing'].play()
        
        crashTest = isCollide(playerx, playery, upperpipes, lowerpipes)
        # This function will return true if player is crashed
        if crashTest:
            return 

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos < playerMidPos < pipeMidPos+4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUND['point'].play()
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX
        
        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperpipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        # If the pipe is out of the screen remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        
        # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['number'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['number'][digit], (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['number'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=="__main__":
    # This will be the main point from where the game will start
    pygame.init() # initialises all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['number'] = (
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('sprites/message.jpg').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load("sprites/pipe.png"), 180),
        pygame.image.load('sprites/pipe.png').convert_alpha()
    )
    GAME_SPRITES['base'] = pygame.image.load("sprites/base.png")
    GAME_SPRITES['player'] = pygame.image.load(PLAYER)
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND)

    # Game Sounds
    GAME_SOUND['die'] = pygame.mixer.Sound('sounds/die.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('sounds/point.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('sounds/wing.wav')

    while True:
        welcomeScreen() # shows welcome screen to the player until button is pressed
        mainGame()  # game starts here