import pygame
import numpy as np
import math

pygame.init()
pygame.font.init()

# font
font = pygame.font.Font("freesansbold.ttf",30)

# colors
white = (255,255,255)
black = (0,0,0)

width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader")

def isCollision(enemyX, enemyY, shotX, shotY):
    distance = math.sqrt( math.pow(enemyX - shotX,2) + math.pow(enemyY - shotY,2) )
    if distance < 27:
        return True
    else:
        return False
    
# player
playerX = width * 0.5
playerY = height * 0.9
playerXChange = 0 # 0 at default
def player(x,y):
    pygame.draw.rect(screen, (0,100,100), [x,y,25,25])

# bullet
shotX = 0
shotY = 0
bullet_state = "ready"
def bullet(x,y):
    pygame.draw.rect(screen, (0,255,0), [x,y,10,10])

# emenies
enemyX = []
enemyY = []
enemyXChange = []
enemyExist = []
enemyNum = 10
for i in range(enemyNum):
    enemyX.append(np.random.randint(0,1000))
    enemyY.append(np.random.randint(0,300))
    enemyXChange.append(2)
    enemyExist.append(True)
    
def enemy(x,y):
    pygame.draw.rect(screen, (136,0,216), [x,y,30,30])


running = True
score = 0
while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("LEFT")
                playerXChange = -2
            elif event.key == pygame.K_RIGHT:
                print("RIGHT")
                playerXChange = 2
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    print("SPACE")
                    shotY = height * 0.9
                    shotX = playerX + 10
                    bullet_state = "fire"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                print("KEYUP")
                playerXChange = 0
                
    playerX += playerXChange
    
    player(playerX,playerY)
    
    for i in range(enemyNum):
        if enemyExist[i] == True:
            enemy(enemyX[i], enemyY[i])
            enemyX[i] += enemyXChange[i]
            if enemyX[i] <= 0:
                enemyXChange[i] = 2
            elif enemyX[i] >= 970:
                enemyXChange[i] = -2
        
        collision = isCollision(enemyX[i], enemyY[i], shotX, shotY)
        if collision:
            # change enemy exist state to the False not to show again
            enemyExist[i] = False
            # reset enemy position
            enemyX[i] = 0
            enemyY[i] = 600
            # reset bullet state and bullet starting position
            bullet_state = "ready"
            shotX = 0
            shotY = 0
            # add score
            score += 1
    # level up judgement
    if enemyExist == [False for i in range(enemyNum)]:
        print("CLEAR")
        clear_font = font.render("GAME CLEAR", True, (255,255,255))
        screen.blit(clear_font, (width/2-100, height/2))
        newgame_font = font.render("NEW GAME", True, (255,255,255))
        screen.blit(newgame_font, (width/2+200, height/2))
        
    if shotY <= 0:
        bullet_state = "ready"
        shotY = 0
    
    if shotY > 0:
        bullet(shotX, shotY)
        shotY -= 5
    
    score_font = font.render("Score : "+str(score), True, (255,255,255))
    screen.blit(score_font, (10,10))
        
    
    pygame.display.update()


pygame.quit()
