import pygame
#importing pygames
import random
import math
from pygame import mixer

pygame.init()
#creating the screen
screen = pygame.display.set_mode((800,600))

#Background
back = open("pictures/background.jpg","r")
background = pygame.image.load(back)

#Background Sounds
mixer.music.load('background.wav')
mixer.music.play(-1)

#player
play = open("pictures/player.png","r")
playerImg = pygame.image.load(play)
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies): 
    enem = open("pictures/enemy.png","r")
    enemyImg.append(pygame.image.load(enem))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

#bullet
bull = open("pictures/bullet.png","r")
bulletImg = pygame.image.load(bull)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#GAme over font
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    
def player(x, y):
    screen.blit(playerImg, (x, y))
    
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
#title and icon
pygame.display.set_caption("Space Invaders")
ufo = open("pictures/ufo.png","r")
icon = pygame.image.load(ufo)
pygame.display.set_icon(icon)

#game loop
running = True
while running:
    screen.fill((0 ,0 ,0))
    #Background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #movement of player 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    #bullet follow path
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
       
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
    #checking for boundries for spaceship
    playerX += playerX_change
    
    if playerX <= 0:
        playerX  = 0
    elif playerX >= 736:
        playerX = 736
    
    #enemy movement
    for i in range(num_of_enemies):
        
        #GAme Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            
            game_over_text()
            # Play the sound
            
            gameover_Sound = mixer.Sound('gameover.wav')
            gameover_Sound.play()
            break
        
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value +=1 
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)
        
    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX,playerY)
    show_score(textX, textY)
    
    pygame.display.update()
