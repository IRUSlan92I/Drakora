"""
Cloud entity class
"""


import pygame
import random


class Cloud(pygame.sprite.Sprite):
    def __init__(self, mainGameClass, cloudType):
        pygame.sprite.Sprite.__init__(self)

        self.type = cloudType
        self.mainGameClass = mainGameClass

        self.image = pygame.Surface((random.randint(150, 350),
                                     random.randint(50, 150)))

        color = 255 - 15 * (3-cloudType)
        self.image.fill((color, color, color))

        self.rect = self.image.get_rect()
        self.rect.center = (
            self.mainGameClass.getScreenWidth() + self.rect.width,
            self.mainGameClass.getScreenHeight()/2 - random.randint(100,
                self.mainGameClass.getScreenHeight()/2-100) + 50*(2-cloudType)
        )

        self.__doubleX = float(self.rect.x)


    def update(self):
        if (self.rect.x < -self.rect.width):
            self.kill()

        self.__doubleX -= self.type*self.mainGameClass.getGameSpeed() / 6
        self.rect.x = self.__doubleX
