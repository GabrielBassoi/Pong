import math
import random

import pygame
import sys
from time import sleep

pygame.init()

LARGURA = 1600
ALTURA = 707
PAD_WIDTH = 16
PAD_HEIGHT = 150
BALL_SPEED = 8
BALL_SIZE = 16
PAD_SPEED = 8

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("MEU JOGO")
clock = pygame.time.Clock()

canhoes1 = []
canhoes2 = []

IMAGEMFUNDO = pygame.image.load("background.png")
IMAGEMCANHAO = pygame.image.load("canhao.png")
TELA.blit(IMAGEMFUNDO, (0,0))

y1 = 0
y2 = 0
velocidade = 20


class Player:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.w = PAD_WIDTH
        self.h = PAD_HEIGHT
        self.color = color
        self.up = False
        self.down = False

    def draw(self):
        pygame.draw.rect(TELA, self.color, pygame.Rect(self.x, self.y, self.w, self.h))

    def reset(self):
        self.y = 300

class Canhao:
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.image = image

    def draw(self):
        TELA.blit(self.image, (self.x, self.y))


class Ball:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (lambda: 180 if random.randint(-1, 1) else 360)()
        self.speed = BALL_SPEED
        self.w = BALL_SIZE
        self.h = BALL_SIZE

    def reset(self):
        self.x = (LARGURA / 2) - (BALL_SIZE / 2)
        self.y = (ALTURA / 2) - (BALL_SIZE / 2)
        self.direction = (lambda: 180 if random.randint(-1, 1) else 360)()
        self.speed = BALL_SPEED

    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
        self.speed *= 1.05

    def draw(self):
        pygame.draw.rect(TELA, (0, 0, 0), pygame.Rect(self.x, self.y, self.w, self.h))


def collision(a, b):
    h_overlaps = True
    v_overlaps = True
    if (a.x > (b.x + b.w)) or ((a.x + a.w) < b.x):
        h_overlaps = False
    if (a.y > (b.y + b.h)) or ((a.y + a.h) < b.y):
        v_overlaps = False
    return h_overlaps and v_overlaps


def show_win_screen(t):
    text = pygame.font.SysFont("verdana", 50, True)

    if t:
        TELA.fill(color=(0, 0, 100))
        TELA.blit(text.render("O Reino Azul ganhou", True, (0, 0, 0)), (LARGURA/2, ALTURA/2))
    else:
        TELA.fill(color=(100, 0, 0))
        TELA.blit(text.render("O Reino Vermelho ganhou", True, (0, 0, 0)), (LARGURA/2, ALTURA/2))

    pygame.display.flip()
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def score():
    if BALL.x < 50:
        BALL.reset()
        canhoes1.pop()
    elif BALL.x > LARGURA-50:
        BALL.reset()
        canhoes2.pop()
    if len(canhoes2) == 0:
        # Time Vermelho ganhou
        show_win_screen(False)
        startCanhoes()
        BALL.reset()
        PLAYER1.reset()
        PLAYER2.reset()
    if len(canhoes1) == 0:
        # Time Azul ganhou
        show_win_screen(True)
        startCanhoes()
        BALL.reset()
        PLAYER1.reset()
        PLAYER2.reset()


def limits():
    if PLAYER1.up and PLAYER1.y > 0:
        PLAYER1.y -= PAD_SPEED
    elif PLAYER1.down and PLAYER1.y+PAD_HEIGHT < ALTURA:
        PLAYER1.y += PAD_SPEED
    if PLAYER2.up and PLAYER2.y > 0:
        PLAYER2.y -= PAD_SPEED
    elif PLAYER2.down and PLAYER2.y+PAD_HEIGHT < ALTURA:
        PLAYER2.y += PAD_SPEED


def bouncTheBall():
    direction_radians = math.radians(BALL.direction)
    BALL.x += BALL.speed * math.cos(direction_radians)
    BALL.y -= BALL.speed * math.sin(direction_radians)

    if BALL.y <= 0:
        BALL.direction = (360 - BALL.direction) % 360
    elif BALL.y > ALTURA - BALL.w:
        BALL.direction = (360 - BALL.direction) % 360
    if collision(PLAYER1, BALL):
        BALL.diff = ((PLAYER1.y + PLAYER1.h) / 2) - ((BALL.y + BALL.h) / 2)
        BALL.bounce(BALL.diff)
    elif collision(PLAYER2, BALL):
        BALL.diff = ((PLAYER2.y + PLAYER2.h) / 2) - ((BALL.y + BALL.h) / 2)
        BALL.bounce(BALL.diff)


def keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        PLAYER1.down = False
        PLAYER1.up = True
    if keys[pygame.K_s]:
        PLAYER1.down = True
        PLAYER1.up = False
    if keys[pygame.K_UP]:
        PLAYER2.down = False
        PLAYER2.up = True
    if keys[pygame.K_DOWN]:
        PLAYER2.down = True
        PLAYER2.up = False


def startCanhoes():
    s = ALTURA / 5
    img = pygame.transform.flip(IMAGEMCANHAO, flip_x=True, flip_y=False)
    for n in range(5):
        canhoes1.append(Canhao(IMAGEMCANHAO, 10, s * n + 50))
    for n in range(5):
        canhoes2.append(Canhao(img, 1540, s * n + 50))

startCanhoes()
PLAYER1 = Player((255, 0, 0), 130, 300)
PLAYER2 = Player((0, 0, 255), 1600-PAD_WIDTH-130, 300)
BALL = Ball(LARGURA/2, ALTURA/2)

is_running = True
while is_running:
    clock.tick(60)
    pygame.display.update()
    score()
    bouncTheBall()
    keys()
    limits()
    TELA.blit(IMAGEMFUNDO, (0, 0))
    BALL.draw()
    PLAYER1.draw()
    PLAYER2.draw()
    for c in canhoes1:
        c.draw()
    for c in canhoes2:
        c.draw()
    pygame.display.update()


