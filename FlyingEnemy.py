"""
Flying enemy entity class
"""


import pygame
import random
import math
import os

from Enemy import Enemy
from CollisionBox import CollisionBox


class FlyingEnemy(Enemy):
    imgDir = os.path.join(os.path.dirname(__file__), 'data')
    senemyImage = pygame.image.load(
        os.path.join(imgDir, 'fenemy.png')
    )#.convert()
    images = (
        pygame.transform.scale(senemyImage.subsurface((0, 0, 16, 8)),(64, 32)),
        pygame.transform.scale(senemyImage.subsurface((16, 0, 16, 8)),(64, 32)),
        pygame.transform.scale(senemyImage.subsurface((32, 0, 16, 8)),(64, 32)),
    )
    for image in images:
        image.set_colorkey((255,0,255))


    def __init__(self, mainGameClass):
        Enemy.__init__(self, mainGameClass)

        self.updateCount = 0
        self.currentImage = 0

        self.subtype = random.randint(1, 10)

        self.image = FlyingEnemy.images[self.currentImage]

        self.rect = self.image.get_rect()
        self.height -= self.rect.height/2 + 10 + 10*self.subtype

        self.rect.center = (mainGameClass.getScreenWidth() + self.rect.width,
                            self.height)

        collision = CollisionBox(2, 0, self.rect.w - 28, self.rect.h - 8, self.rect.center)
        self.collisionBoxes.add(collision)

        self.speed = self.thisGame.getGameSpeed()*2


    def update(self):
        super().update()

        self.updateCount += 1
        if self.updateCount >= 22 - math.log2(self.thisGame.getGameSpeed()) * 2:
            self.currentImage += 1
            if self.currentImage >= len(FlyingEnemy.images):
                self.currentImage = 0
            self.image = FlyingEnemy.images[self.currentImage]
            self.updateCount = 0
