"""
Background layer frame entity class
"""


import pygame


class BackgroundLayerFrame(pygame.sprite.Sprite):
    def __init__(self, image, mainGameClass, offset, speedMultiplier):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.mainGameClass = mainGameClass
        self.speedMultiplier = speedMultiplier

        self.rect = self.image.get_rect()
        self.rect.center = (mainGameClass.getScreenWidth()/2 + offset[0],
                            mainGameClass.getScreenHeight()/2 + offset[1])

        self.__doubleX = float(self.rect.x)


    def update(self):
        self.__doubleX -= self.mainGameClass.getGameSpeed() * self.speedMultiplier
        if self.__doubleX < -self.rect.width:
            self.__doubleX += self.rect.width*2

        self.rect.x = self.__doubleX
