import numpy as np
import pygame
import math
import time

pygame.init()
pygame.font.init()

class Invader:
    def __init__(self, width=1000, height=600):
        self.font = pygame.font.Font("freesansbold.ttf",30)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    # functions
    def isCollision(self):
        pass

    def player(self,x,y):
        pygame.draw.rect(self.screen, (255,255,255), [x,y,40,40])

    def bullet(self,x,y):
        pygame.draw.rect(self.screen, (0,255,0), [x+15,y-5,10,10])

    def isCollision(self, enemyX, enemyY, shotX, shotY):
        distance = math.sqrt( math.pow(enemyX - shotX, 2) + math.pow(enemyY - shotY, 2))
        if distance < 27:
            return True
        else:
            return False

    def enemy(self,x,y):
        pygame.draw.rect(self.screen, (136,0,216), [x,y,30,30])

    def game_main(self, enemyNum, timeLimmit):
        pygame.display.set_caption("Space Invader")
        # players position
        playerX = self.width / 2
        playerY = self.height * 0.9
        playerXChange = 0

        # bullet
        shotX = 0
        shotY = 0
        bullet_state = "ready"

        # enemy
        enemyX = []
        enemyY = []
        enemyXChange = []
        enemyExist = []
        for i in range(enemyNum,timeLimmit):
            enemyX.append(np.random.randint(0,1000))
            enemyY.append(np.random.randint(0,300))
            enemyXChange.append(2)
            enemyExist.append(True)

        # game loop
        running = True
        score = 0
        start_time = time.time()
        crash = "NO"
        while running:
            current_time = time.time()
            if current_time - start_time >= timeLimmit:
                print("TIME OVER")
                # by this code, able to go through clear judgement
                enemyExist = [False for i in range(enemyNum)]
                crash = "YES"

            self.screen.fill((0,0,0))
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
                            shotY = self.height * 0.9
                            shotX = playerX
                            bullet_state = "fire"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        print("KEYUP")
                        playerXChange = 0

            playerX += playerXChange
            # player
            self.player(playerX, playerY)
            if playerX < 0:
                playerX = 0
            elif playerX >= 960:
                playerX = 960

            # enemy
            for i in range(enemyNum):
                if enemyExist[i] == True:
                    self.enemy(enemyX[i], enemyY[i])
                    enemyX[i] += enemyXChange[i]
                    if enemyX[i] <= 0:
                        enemyXChange[i] = 2
                    elif enemyX[i] >= 970:
                        enemyXChange[i] = -2
                collision = self.isCollision(enemyX[i], enemyY[i], shotX, shotY)
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
                self.bullet(shotX, shotY)
                shotY -= 5

            # clear judgement
            if enemyExist == [False for i in range(enemyNum)]:
                if crash == "NO":
                    print("Clear")
                    clear_font = self.font.render("GAME CLEAR", True, (255,255,255))
                    self.screen.blit(clear_font, (self.width/2-100, self.height/2))
                elif crash == "YES":
                    print("GAME OVER")
                    gameover_font = self.font.render("GAME OVER", True, (255,255,255))
                    self.screen.blit(gameover_font, (self.width/2-100, self.height/2))

            score_font = self.font.render("Score : " + str(score), True, (255,255,255))
            self.screen.blit(score_font, (10,10))
            
            remain_time = int(timeLimmit - (current_time - start_time))
            if remain_time < 0:
                remain_time = 0
            remain_time_font = self.font.render("Remain Time : " + str(remain_time), True, (255,255,255))
            self.screen.blit(remain_time_font, (10, 50))

            pygame.display.update()

    def main(self):
        level = 1
        cleared = True
        while cleared:
            print("Level :",level)
            enemyNum = level * 3
            timeLimmit = level * 10
            clear = self.game_main(enemyNum,timeLimmit)
            if clear == False:
                cleared = False

            
invader = Invader()
invader.game_main(3,20)
