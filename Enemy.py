"""
Enemy entity class
"""


import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, mainGameClass):
        pygame.sprite.Sprite.__init__(self)

        self.thisGame = mainGameClass

        self.height = (mainGameClass.getScreenHeight()
                        - mainGameClass.getFloorHeight())

        self.collisionBoxes = pygame.sprite.Group()


    def getCollisionBoxes(self):
        return self.collisionBoxes


    def update(self):
        if (self.rect.x < -self.rect.width):
            self.kill()
            self.thisGame.addScore(1)

        self.rect.x -= self.speed

        for i in self.collisionBoxes:
            i.setX(self.rect.x)
