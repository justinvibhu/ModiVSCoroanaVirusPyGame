import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
# title and ICon
pygame.display.set_caption("Corona Crash")
icon = pygame.image.load('img/virus.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('img/player2.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# background
# background = pygame.image.load('player1.png')
# bcak music
mixer.music.load('sound/gamemusic.mp3')
mixer.music.play(-1)

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('img/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))

    enemyX_change.append(0.5)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480

bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


# game over

def game_over_text():
    over_text = pygame.image.load("img/gameover.png")
    screen.blit(over_text, (0, 0))


def shw_score(x, y):
    sco = font.render("NAMO NAMO", True, (255, 255, 255))
    screen.blit(sco, (x, y))

    score = font.render("score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x + 20, y + 30))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 16))


# gameloop

running = True
while running:
    screen.fill((0, 0, 0))

    #  screen.blit(background, (0, 0))  # 800*600

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # movent of player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('sound/bullet.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # boundaries of window
    playerX += playerX_change

    if playerX <= 0 :
        playerX = 0


    elif playerX >= 736 :
        playerX = 736
        playerY =480


    # enemy movement
    for i in range(num_of_enemy):
        # text
        # level up
        if score_value >= 100:

            if enemyX[i] <= 0:
                enemyX_change[i] = 0.7
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.7
                enemyY[i] += enemyY_change[i]
            while (score_value == 150):
                break

        if enemyY[i] > 480:
            for i in range(num_of_enemy):
                enemyY[i] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('sound/kill.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerY += playerY_change
    player(playerX, playerY)
    shw_score(textX, textY)
    pygame.display.update()
