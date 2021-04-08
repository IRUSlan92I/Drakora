"""
Cloud entity class
"""


import pygame
import random


class Cloud(pygame.sprite.Sprite):
    def __init__(self, mainGameClass, cloudType):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((random.randint(150, 350),
                                     random.randint(50, 150)))

        color = 255 - 15 * (3-cloudType)
        self.image.fill((color, color, color))

        self.rect = self.image.get_rect()
        self.rect.center = (
            mainGameClass.getScreenWidth() + self.rect.width,
            mainGameClass.getScreenHeight()/2 - random.randint(100,
                mainGameClass.getScreenHeight()/2-100) + 50*(2-cloudType)
        )
        self.speed = cloudType*mainGameClass.getGameSpeed() / 6

        self.__doubleX = float(self.rect.x)


    def update(self):
        if (self.rect.x < -self.rect.width):
            self.kill()

        self.__doubleX -= self.speed
        self.rect.x = self.__doubleX
