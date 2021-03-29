"""
Main game class
"""


import pygame
import random

from Player import Player
from Enemy import Enemy
from Cloud import Cloud
from Floor import Floor


class Drakora():
    def getGameSpeed(self):
        return self.__gameSpeed


    def getScore(self):
        return self.__score


    def getScreenWidth(self):
        return self.screenSize[0]


    def getScreenHeight(self):
        return self.screenSize[1]


    def getFloorHeight(self):
        return self.floorHeight


    def addScore(self, score):
        self.__score += score

        if self.__score%self.speedUpRate == 0:
            self.__gameSpeed += 1
            self.speedUpLabelCD = self.targetFps


    def newGame(self):
        for enemy in self.enemies:
            enemy.kill()

        if self.player: self.player.kill()

        self.player = Player()
        self.sprites.add(self.player)

        self.__score = 0
        self.isGameOver = False
        self.isPaused = False

        self.__gameSpeed = 2

        self.enemyCount = 0
        self.enemyCD = self.getNextEnemyCD()
        self.enemyChance = 100.0

        self.speedUpLabelCD = 0


    def __init__(self):
        self.buttonsPause = (pygame.K_p,)
        self.buttonsQuit = (pygame.K_F10,)
        self.buttonsNewGame = (pygame.K_RETURN,)

        self.screenSize = (800, 600)
        self.targetFps = 120

        self.floorHeight = 50

        self.floors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.player = None

        self.speedUpRate = 25

        self.godmodeCount = 0
        self.isGodmode = False

        random.seed()
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption('Drakora')
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()
        self.floors.add(Floor(self))
        self.sprites.add(self.floors)

        font = pygame.font.match_font('liberation mono')
        self.fontScore = pygame.font.Font(font, 32)
        self.fontMessage = pygame.font.Font(font, 56)
        self.fontGodmode = pygame.font.Font(font, 12)

        self.newGame()


    def __del__(self):
        pygame.quit()


    def renderText(self, text, font, color, center):
        render = font.render(text, True, color)
        rect = render.get_rect()
        rect.center = center
        self.screen.blit(render, rect)


    def render(self):
        self.screen.fill((102, 153, 255))
        self.sprites.draw(self.screen)
        self.floors.draw(self.screen)

        self.renderText('%d'%(self.__score),
                        self.fontScore, (255, 255, 255),
                         (self.getScreenWidth()/2,20))

        if self.isGameOver:
            self.renderText('GAME OVER',
                            self.fontMessage, (255, 255, 255),
                            tuple(i/2 for i in self.screenSize))
        elif self.isPaused:
            self.renderText('PAUSED',
                            self.fontMessage, (255, 255, 255),
                            tuple(i/2 for i in self.screenSize))
        elif self.speedUpLabelCD > 0:
            self.speedUpLabelCD -= 1
            self.renderText('SPEED UP',
                            self.fontMessage, (255, 255, 255),
                            tuple(i/2 for i in self.screenSize))

        if self.isGodmode:
            self.renderText('godmode',
                            self.fontGodmode, (255, 255, 255),
                            (self.getScreenWidth()/2,40))

        pygame.display.flip()


    def getNextEnemyCD(self):
        if self.enemyCount <= 5:
            return 1000
        elif self.enemyCount <= 5:
            return 800 - 100*self.enemyCount
        elif self.enemyCount%self.speedUpRate == 0:
            return 1000
        else:
            return 300


    def collideCheck(self):
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            if not self.isGodmode: self.isGameOver = True

        self.player.isOnFloor = False

        while pygame.sprite.spritecollideany(self.player, self.floors):
            self.player.isOnFloor = True
            self.player.rect.y -= 1


    def logic(self):
        for event in pygame.event.get():
            self.player.control(event)

            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key in self.buttonsQuit:
                    return False
                elif event.key in self.buttonsNewGame:
                    if self.isGameOver: self.newGame()
                elif event.key in self.buttonsPause:
                    self.isPaused = not self.isPaused

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    if self.godmodeCount == 0:  self.godmodeCount += 1
                    else:                       self.godmodeCount == 0
                elif event.key == pygame.K_o:
                    if (self.godmodeCount == 1 or
                       self.godmodeCount == 4): self.godmodeCount += 1
                    else:                       self.godmodeCount == 0
                elif event.key == pygame.K_d:
                    if (self.godmodeCount == 2 or
                       self.godmodeCount == 5): self.godmodeCount += 1
                    else:                       self.godmodeCount == 0
                elif event.key == pygame.K_m:
                    if self.godmodeCount == 3:  self.godmodeCount += 1
                    else:                       self.godmodeCount == 0
                elif event.key == pygame.K_e:
                    if self.godmodeCount == 6:
                        self.godmodeCount == 0
                        self.isGodmode = not self.isGodmode
                else:
                    self.godmodeCount = 0

        if not self.isGameOver and not self.isPaused:
            self.sprites.update()

            self.enemyCD -= self.__gameSpeed

            if random.randint(1, 200) == 1:
                cloud = Cloud(self)
                self.clouds.add(cloud)
                self.sprites.add(cloud)

            if self.enemyCD <= 0:
                self.enemyChance += (1/self.targetFps) * self.enemyChance/8

                if random.randint(1, 150) < self.enemyChance:
                    self.enemyCount += 1
                    self.enemyCD = self.getNextEnemyCD()
                    self.enemyChance = 1
                    enemy = Enemy(self)
                    self.enemies.add(enemy)
                    self.sprites.add(enemy)

        self.collideCheck()

        return True


    def play(self):
        isRunning = True
        while isRunning:
            self.clock.tick(self.targetFps)
            self.render()
            isRunning = self.logic()


if __name__ == '__main__':
    drakora = Drakora()
    drakora.play()
    del Drakora
