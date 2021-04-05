"""
Standing enemy entity class
"""


import pygame
import random
import os

from Enemy import Enemy


class StandingEnemy(Enemy):
    imgDir = os.path.join(os.path.dirname(__file__), 'data')
    senemyImage = pygame.image.load(os.path.join(imgDir, 'senemy.png'))#.convert()
    images = (
        (
            pygame.transform.scale(senemyImage.subsurface((0, 0, 8, 24)), (32, 98)),
            pygame.transform.scale(senemyImage.subsurface((8, 0, 8, 24)), (32, 98)),
            pygame.transform.scale(senemyImage.subsurface((16, 0, 8, 24)), (32, 98)),
            pygame.transform.scale(senemyImage.subsurface((24, 0, 8, 24)), (32, 98)),
            pygame.transform.scale(senemyImage.subsurface((32, 0, 8, 24)), (32, 98)),
            pygame.transform.scale(senemyImage.subsurface((40, 0, 8, 24)), (32, 98)),
        ),
        (
            pygame.transform.scale(senemyImage.subsurface((0, 24, 8, 16)), (32, 64)),
            pygame.transform.scale(senemyImage.subsurface((8, 24, 8, 16)), (32, 64)),
            pygame.transform.scale(senemyImage.subsurface((16, 24, 8, 16)), (32, 64)),
            pygame.transform.scale(senemyImage.subsurface((24, 24, 8, 16)), (32, 64)),
            pygame.transform.scale(senemyImage.subsurface((32, 24, 8, 16)), (32, 64)),
            pygame.transform.scale(senemyImage.subsurface((40, 24, 8, 16)), (32, 64)),
        ),
        (
            pygame.transform.scale(senemyImage.subsurface((0, 40, 16, 16)), (64, 64)),
            pygame.transform.scale(senemyImage.subsurface((16, 40, 16, 16)), (64, 64)),
            pygame.transform.scale(senemyImage.subsurface((32, 40, 16, 16)), (64, 64)),
            pygame.transform.scale(senemyImage.subsurface((0, 56, 16, 16)), (64, 64)),
            pygame.transform.scale(senemyImage.subsurface((16, 56, 16, 16)), (64, 64)),
            pygame.transform.scale(senemyImage.subsurface((32, 56, 16, 16)), (64, 64)),
        ),
        (
            pygame.transform.scale(senemyImage.subsurface((0, 72, 8, 8)), (32, 32)),
            pygame.transform.scale(senemyImage.subsurface((8, 72, 8, 8)), (32, 32)),
            pygame.transform.scale(senemyImage.subsurface((16, 72, 8, 8)), (32, 32)),
            pygame.transform.scale(senemyImage.subsurface((24, 72, 8, 8)), (32, 32)),
            pygame.transform.scale(senemyImage.subsurface((32, 72, 8, 8)), (32, 32)),
            pygame.transform.scale(senemyImage.subsurface((40, 72, 8, 8)), (32, 32)),
        ),
        (
            pygame.transform.scale(senemyImage.subsurface((0, 80, 16, 8)), (64, 32)),
            pygame.transform.scale(senemyImage.subsurface((16, 80, 16, 8)), (64, 32)),
            pygame.transform.scale(senemyImage.subsurface((32, 80, 16, 8)), (64, 32)),
            pygame.transform.scale(senemyImage.subsurface((0, 88, 16, 8)), (64, 32)),
            pygame.transform.scale(senemyImage.subsurface((16, 88, 16, 8)), (64, 32)),
            pygame.transform.scale(senemyImage.subsurface((32, 88, 16, 8)), (64, 32)),
        ),
        (
            pygame.transform.scale(senemyImage.subsurface((0, 96, 24, 8)), (98, 32)),
            pygame.transform.scale(senemyImage.subsurface((24, 96, 24, 8)), (98, 32)),
            pygame.transform.scale(senemyImage.subsurface((0, 104, 24, 8)), (98, 32)),
            pygame.transform.scale(senemyImage.subsurface((24, 104, 24, 8)), (98, 32)),
            pygame.transform.scale(senemyImage.subsurface((0, 112, 24, 8)), (98, 32)),
            pygame.transform.scale(senemyImage.subsurface((24, 112, 24, 8)), (98, 32)),
        ),
    )


    def __init__(self, mainGameClass):
        Enemy.__init__(self, mainGameClass)

        for array in self.images:
            for image in array:
                image.set_colorkey((255,0,255))


        self.subtype = random.randint(1, len(StandingEnemy.images))

        self.image = random.choice(StandingEnemy.images[self.subtype-1])

        # if   self.subtype == 1: self.image = pygame.Surface((32, 96))
        # elif self.subtype == 2: self.image = pygame.Surface((32, 64))
        # elif self.subtype == 3: self.image = pygame.Surface((64, 64))
        # elif self.subtype == 4: self.image = pygame.Surface((32, 32))
        # elif self.subtype == 5: self.image = pygame.Surface((64, 32))
        # else:                   self.image = pygame.Surface((96, 32))

        # self.image.fill((0, 153, 0))
        self.rect = self.image.get_rect()
        self.height -= self.rect.height/2

        self.rect.center = (mainGameClass.getScreenWidth() + self.rect.width,
                            self.height)

        self.speed = self.thisGame.getGameSpeed()
