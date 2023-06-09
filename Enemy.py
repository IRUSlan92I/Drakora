"""
Enemy entity class
"""


import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, mainGameClass):
        pygame.sprite.Sprite.__init__(self)

        self.mainGameClass = mainGameClass

        self.height = (mainGameClass.getScreenHeight()
                        - mainGameClass.getFloorHeight())

        self.collisionBoxes = pygame.sprite.Group()


    def getCollisionBoxes(self):
        return self.collisionBoxes


    def update(self):
        if (self.rect.x < -self.rect.width):
            self.kill()
            self.mainGameClass.addScore(1)
        else:
            self.doubleX -= self.speed
            self.rect.x = self.doubleX

            for i in self.collisionBoxes:
                i.setX(self.rect.x)
