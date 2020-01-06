import pygame
import numpy as np
import math
import time

pygame.init()
pygame.font.init()

# font
font = pygame.font.Font("freesansbold.ttf", 30)


width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SPACE INVADER")

# collision
def isCollision(enemyX, enemyY, shotX, shotY):
    distance = math.sqrt( math.pow(enemyX - shotX,2) + math.pow(enemyY - shotY,2) )
    if distance < 27:
        return True
    else:
        return False

# player
playerX = width * 0.5
playerY = height * 0.9
playerXChange = 0
def player(x,y):
    pygame.draw.rect(screen, (0,100,100), [x,y,25,25])

# bullet
shotX = 0
shotY = 0
bullet_state = "ready"
def bullet(x,y):
    pygame.draw.rect(screen, (0,255,0), [x,y,10,10])

# enemies
enemyX = []
enemyY = []
enemyXChange = []
enemyExist = []
enemyNum = 1
for i in range(enemyNum):
    enemyX.append(np.random.randint(0,975))
    enemyY.append(np.random.randint(0,300))
    enemyXChange.append(2)
    enemyExist.append(True)
def enemy(x,y):
    pygame.draw.rect(screen, (136,0,216), [x,y,30,30])


running = True
timer_stop = False
clear_time = 0
score = 0
start_time = time.time()
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -2
            elif event.key == pygame.K_RIGHT:
                playerXChange = 2
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    shotY = height * 0.9 + 10
                    shotX = playerX
                    bullet_state = "fire"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0
    # player
    playerX += playerXChange
    player(playerX, playerY)
    if playerX <= 0:
        playerX = 0
    elif playerX >= 975:
        playerX = 975

    # enemies
    for i in range(enemyNum):
        if enemyExist[i] == True:
            enemy(enemyX[i], enemyY[i])
            enemyX[i] += enemyXChange[i]
            if enemyX[i] <= 0:
                enemyXChange[i] = 2
            elif enemyX[i] >= 975:
                enemyXChange[i] = -2
        collision = isCollision(enemyX[i], enemyY[i], shotX, shotY)
        if collision:
            enemyExist[i] = False
            enemyX[i] = 0
            enemyY[i] = 600
            bullet_state = "ready"
            shotX = 0
            shotY = 0
            score += 1

    # bullet
    if shotY <= 0:
        bullet_state = "ready"
        shotY = 0
    if shotY > 0:
        bullet(shotX, shotY)
        shotY -= 5
    
    # clear judgement
    if enemyExist == [False for i in range(enemyNum)]:
        clear_font = font.render("GAME CLEAR", True, (255,255,255))
        screen.blit(clear_font, (width/2-100, height/2))
        if timer_stop == False: # timer not stopped
            clear_time = time.time() - start_time
            #clear_time_font = font.render("Clear Time : " + str(clear_time), True, (255,255,255))
            #screen.blit(clear_time_font, (width/2-100, height* 0.8))
            timer_stop = True

    # timer
    current_time = time.time()
    timer = current_time - start_time
    #time_font = font.render("Time : " + str(timer), True, (255,255,255))
    #screen.blit(time_font, (10,60))

    if timer_stop == True:
        clear_time_font = font.render("Clear Time : " + str(clear_time), True, (255,255,255))
        screen.blit(clear_time_font, (width/2-190, height*0.6))
        time_font = font.render("Time : " + str(clear_time), True, (255,255,255))
    else:
        time_font = font.render("Time : " + str(timer), True, (255,255,255))
    
    screen.blit(time_font, (10,60))

    score_font = font.render("Score : "+str(score), True, (255,255,255))
    screen.blit(score_font, (10,10))

    pygame.display.update()

pygame.quit()
