"""
Standing enemy entity class
"""


import pygame
import random
from Enemy import Enemy


class StandingEnemy(Enemy):
    def __init__(self, mainGameClass):
        Enemy.__init__(self, mainGameClass)

        self.subtype = random.randint(1, 5)

        if   self.subtype == 1: self.image = pygame.Surface((25, 75))
        elif self.subtype == 2: self.image = pygame.Surface((25, 25))
        elif self.subtype == 3: self.image = pygame.Surface((75, 25))
        elif self.subtype == 4: self.image = pygame.Surface((50, 25))
        elif self.subtype == 5: self.image = pygame.Surface((50, 50))
        else:                   self.image = pygame.Surface((25, 50))

        self.image.fill((0, 153, 0))
        self.rect = self.image.get_rect()
        self.height -= self.rect.height/2

        self.rect.center = (mainGameClass.getScreenWidth() + self.rect.width,
                            self.height)

        self.speed = self.thisGame.getGameSpeed()
