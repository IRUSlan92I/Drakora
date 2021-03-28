"""
Enemy entity class
"""


import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def setNextEnemyType(self, score):
        if score < 10:
            self.type = 1

        elif score < 20:
            if random.randint(1, 100) < 95: self.type = 1
            else:                           self.type = 2

        elif score < 40:
            if random.randint(1, 100) < 85: self.type = 1
            else:                           self.type = 2

        else:
            if random.randint(1, 100) < 75: self.type = 1
            else:                           self.type = 2


    def setNextEnemySubtype(self):
        if self.type == 1:
            self.subtype = random.randint(1, 5)
        elif self.type == 2:
            self.subtype = random.randint(1, 7)


    def __init__(self, mainGameClass):
        pygame.sprite.Sprite.__init__(self)

        self.thisGame = mainGameClass

        self.speed = self.thisGame.getGameSpeed()

        self.setNextEnemyType(self.thisGame.getScore())
        self.setNextEnemySubtype()

        self.height = mainGameClass.getScreenHeight() - mainGameClass.floorHeight

        if self.type == 1:
            if self.subtype == 1:   self.image = pygame.Surface((25, 75))
            elif self.subtype == 2: self.image = pygame.Surface((25, 25))
            elif self.subtype == 3: self.image = pygame.Surface((75, 25))
            elif self.subtype == 4: self.image = pygame.Surface((50, 25))
            elif self.subtype == 5: self.image = pygame.Surface((50, 50))
            else:                   self.image = pygame.Surface((25, 50))

            self.image.fill((0, 153, 0))
            self.rect = self.image.get_rect()
            self.height -= self.rect.height/2

        elif self.type == 2:
            self.image = pygame.Surface((50, 25))
            self.image.fill((51, 51, 0))
            self.rect = self.image.get_rect()
            self.height -= self.rect.height/2 + 10 + 10*self.subtype

        self.rect.center = (mainGameClass.getScreenWidth() + self.rect.width,
                            self.height)


    def update(self):
        if (self.rect.x < -self.rect.width):
            self.kill()
            self.thisGame.addScore(1)

        if self.type == 1:
            self.rect.x -= self.speed
        else:
            self.rect.x -= self.speed*2
