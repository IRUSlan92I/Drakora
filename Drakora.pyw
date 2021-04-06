"""
Main game class
"""


import pygame
import random
import os

from collections import deque

from Background import Background
from Player import Player
from StandingEnemy import StandingEnemy
from FlyingEnemy import FlyingEnemy
from Cloud import Cloud
from Floor import Floor
from EndSceen import EndSceen


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


    def speedUp(self):
        self.__gameSpeed += 1.5


    def speedDown(self):
        if self.__gameSpeed > 1.5: self.__gameSpeed -= 1.5


    def speedReset(self):
        self.__gameSpeed = 1.5


    def addScore(self, score):
        self.__score += score

        if self.__score%self.speedUpRate == 0:
            self.speedUp()
            self.speedUpLabelCD = self.targetFps

    def getFont(self):
        return self.font


    def getTime(self):
        return self.time


    def newGame(self):
        self.background = Background(self)

        for enemy in self.enemies:
            enemy.kill()

        for cloudGroup in self.cloudGroups:
            for cloud in cloudGroup:
                cloud.kill()

        if self.player: self.player.kill()

        self.player = Player(self)
        self.players.add(self.player)

        self.__score = 0
        self.isGameOver = False
        self.isPaused = False

        self.speedReset()

        self.enemyCount = 0
        self.enemyChance = 100.0

        self.speedUpLabelCD = 0
        self.nextEnemyMustBeFlying = False

        self.enemyCD = self.getNextEnemyCD()

        self.speedUpCheatLabelCD = 0
        self.speedDownCheatLabelCD = 0
        self.speedResetCheatLabelCD = 0

        self.time = 0
        self.endSceen.newEndScreen()


    def __init__(self):
        random.seed()
        pygame.init()
        self.screenSize = (800, 600)
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption('Drakora')
        self.clock = pygame.time.Clock()

        self.buttonsPause = (pygame.K_p,)
        self.buttonsQuit = (pygame.K_F10,)
        self.buttonsNewGame = (pygame.K_RETURN,)

        self.targetFps = 120

        self.floorHeight = 64

        self.players = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.cloudGroups = (pygame.sprite.Group(),
                            pygame.sprite.Group(),
                            pygame.sprite.Group(),)
        self.player = None

        self.floors.add(Floor(self))

        self.speedUpRate = 25

        self.godmodeCount = 0
        self.isGodmode = False
        self.drawBoxes = False

        self.font = pygame.font.match_font('liberation mono')
        self.fontScore = pygame.font.Font(self.font, 32)
        self.fontMessage = pygame.font.Font(self.font, 56)
        self.fontGodmode = pygame.font.Font(self.font, 12)

        self.charKeys = tuple(
            pygame.key.key_code(chr(i)) for i in range(ord("a"), ord("z"))
        )

        self.pressedKeys = deque(maxlen=10)
        self.isPressedKeysUpdated = True

        self.endSceen = EndSceen(self)

        self.newGame()


    def __del__(self):
        pygame.quit()


    def renderText(self, text, font, color, center):
        render = font.render(text, True, color)
        rect = render.get_rect()
        rect.center = center
        self.screen.blit(render, rect)


    def render(self):
        self.screen.fill((61, 150, 223))
        for cloudGroup in self.cloudGroups[:2]: cloudGroup.draw(self.screen)
        self.background.draw(self.screen)
        for cloudGroup in self.cloudGroups[2:]: cloudGroup.draw(self.screen)
        self.enemies.draw(self.screen)
        self.players.draw(self.screen)

        if self.drawBoxes:
            for player in self.players:
                for collision in player.getCollisionBoxes():
                    pygame.draw.rect(self.screen, (255, 0, 0), collision.rect, 1)
            for enemy in self.enemies:
                for collision in enemy.getCollisionBoxes():
                    pygame.draw.rect(self.screen, (255, 0, 0), collision.rect, 1)
            for floor in self.floors:
                pygame.draw.rect(self.screen, (255, 0, 0), floor.rect, 1)

        if self.isGameOver:
            self.endSceen.render();
        else:
            self.renderText('%d'%(self.__score),
                            self.fontScore, (255, 255, 255),
                             (self.getScreenWidth()/2,20))

            if self.isPaused:
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

        if self.speedUpCheatLabelCD:
            self.speedUpCheatLabelCD -= 1
            self.renderText('speed up',
                            self.fontGodmode, (255, 255, 255),
                            (self.getScreenWidth()/2,60))

        if self.speedDownCheatLabelCD:
            self.speedDownCheatLabelCD -= 1
            self.renderText('speed down',
                            self.fontGodmode, (255, 255, 255),
                            (self.getScreenWidth()/2,60))

        if self.speedResetCheatLabelCD:
            self.speedResetCheatLabelCD -= 1
            self.renderText('speed reset',
                            self.fontGodmode, (255, 255, 255),
                            (self.getScreenWidth()/2,60))

        pygame.display.flip()


    def getNextEnemyCD(self):
        if self.enemyCount == 0:
            return 1000
        elif self.enemyCount <= 5:
            return 800 - 100*self.enemyCount
        elif self.enemyCount%self.speedUpRate == 0:
            return 1000
        elif self.nextEnemyMustBeFlying:
            return 600
        else:
            return 300

    def collideCheck(self):
        for enemy in self.enemies:
            if pygame.sprite.groupcollide(self.player.getCollisionBoxes(), enemy.getCollisionBoxes(), None, None):
                if not self.isGodmode:
                    self.isGameOver = True
                    break

        if self.player.isOnFloor:
            self.player.rect.y += 1
            if not pygame.sprite.spritecollideany(self.player, self.floors):
                self.player.isOnFloor = False
        else:
            if pygame.sprite.spritecollideany(self.player, self.floors):
                self.player.isOnFloor = True

        if self.player.isOnFloor:
            while pygame.sprite.spritecollideany(self.player, self.floors):
                self.player.rect.y -= 1


    def doCheats(self):
        if self.isPressedKeysUpdated:
            pressedKeysStr = ''.join(self.pressedKeys)

            if pressedKeysStr.endswith('godmode'):
                self.isGodmode = not self.isGodmode
            elif pressedKeysStr.endswith('speedup'):
                self.speedUp()
                self.speedUpCheatLabelCD = 60
            elif pressedKeysStr.endswith('speeddown'):
                self.speedDown()
                self.speedDownCheatLabelCD = 60
            elif pressedKeysStr.endswith('speedreset'):
                self.speedReset()
                self.speedResetCheatLabelCD = 60
            elif pressedKeysStr.endswith('drawboxes'):
                self.drawBoxes = not self.drawBoxes

            self.isPressedKeysUpdated = False


    def logic(self):
        for event in pygame.event.get():
            self.player.control(event)
            self.endSceen.control(event)

            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key in self.buttonsQuit:
                    return False
                elif event.key in self.buttonsNewGame:
                    if self.isGodmode: self.newGame()
                elif event.key in self.buttonsPause:
                    self.isPaused = not self.isPaused

            elif event.type == pygame.KEYUP:
                if event.key in self.charKeys:
                    self.pressedKeys.append(pygame.key.name(event.key))
                    self.isPressedKeysUpdated = True

        self.doCheats()

        if not self.isGameOver and not self.isPaused:
            self.time += 1/self.targetFps
            self.background.update()

            for cloudGroup in self.cloudGroups: cloudGroup.update()
            self.enemies.update()
            self.players.update()
            self.floors.update()

            self.enemyCD -= self.__gameSpeed

            if random.randint(1, 200) == 1:
                cloudType = random.randint(0, 2)
                cloud = Cloud(self, cloudType)
                self.cloudGroups[cloudType].add(cloud)

            if self.enemyCD <= 0:
                self.enemyChance += (1/self.targetFps) * self.enemyChance/8

                if random.randint(1, 150) < self.enemyChance:
                    self.enemyCount += 1
                    self.enemyChance = 1

                    if self.nextEnemyMustBeFlying:
                        enemy = FlyingEnemy(self)
                    else:
                        enemy = StandingEnemy(self)

                    if self.__score < 10:
                        self.nextEnemyMustBeFlying = False

                    elif self.__score < 20:
                        self.nextEnemyMustBeFlying = random.randint(1, 100) > 95

                    elif self.__score < 40:
                        self.nextEnemyMustBeFlying = random.randint(1, 100) > 85

                    else:
                        self.nextEnemyMustBeFlying = random.randint(1, 100) > 75

                    self.enemyCD = self.getNextEnemyCD()

                    self.enemies.add(enemy)

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
