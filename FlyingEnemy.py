"""
Flying enemy entity class
"""


import pygame
import random
from Enemy import Enemy


class FlyingEnemy(Enemy):
    def __init__(self, mainGameClass):
        Enemy.__init__(self, mainGameClass)

        self.subtype = random.randint(1, 7)

        self.image = pygame.Surface((50, 25))
        self.image.fill((51, 51, 0))
        self.rect = self.image.get_rect()
        self.height -= self.rect.height/2 + 10 + 10*self.subtype

        self.rect.center = (mainGameClass.getScreenWidth() + self.rect.width,
                            self.height)

        self.speed = self.thisGame.getGameSpeed()*2
