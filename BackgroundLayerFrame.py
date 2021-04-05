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


    def update(self):
        self.rect.x -= self.mainGameClass.getGameSpeed() * self.speedMultiplier
        if self.rect.x < -self.rect.width:
            self.rect.x += self.rect.width*2
