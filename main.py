import pygame
import random
import math

pygame.init()
from pygame import mixer

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('star wars')

playerImg = pygame.image.load('ttt.png')
playerX = 380
playerY = 370
playerX_change = 0

alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 12

p = 0
playing = True
falling = False
count = 0

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 800))
    alienY.append(random.randint(20, 120))
    alienX_change.append(20)
    alienY_change.append(70)

bulletImg = pygame.image.load('bullet.png')
bulletX = 1000
bulletY = 378
bulletY_change = 28
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('Broken-Detroit - PERSONAL USE ONLY.ttf', 32)

textY = 10
textX = 10

game_font = pygame.font.Font('Broken-Detroit - PERSONAL USE ONLY.ttf', 64)


def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def you_win():
    win_text = game_font.render("YOU WIN", True, (255, 255, 255))
    screen.blit(win_text, (250, 180))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 50, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX, 2) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def fall():
    global falling
    over_text = game_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 180))
    if not falling:
        explosion = mixer.Sound("game oveeer!.wav")
        explosion.play()
        falling = True


running = True
while running:
    clock.tick(52)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    laser = mixer.Sound("laser.wav")
                    laser.play()
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX == 0:
        playerX = 0
    elif playerX >= 690:
        playerX = 690

    for i in range(num_of_aliens):

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 10.2
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX[i] += alienX_change[i]
            alienX_change[i] = -10.2

        if alienY[i] > 350 and alienX[i] >= playerX - 30:
            fall()
            for j in range(num_of_aliens):
                alienY[j] = 3000
            break

        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound("explosion.wav")
            explosion.play()
            bulletY = 370
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 800)
            alienY[i] = random.randint(20, 120)

        alien(alienX[i], alienY[i], i)

    if bulletY <= 0:
        bulletY = 378
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
