"""
Floor entity class
"""


import pygame


class Floor(pygame.sprite.Sprite):
    def __init__(self, mainGameClass):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((mainGameClass.getScreenWidth(),
                                    mainGameClass.getFloorHeight()))
        self.image.fill((255, 204, 102))
        self.rect = self.image.get_rect()
        self.rect.center = (mainGameClass.getScreenWidth()/2,
                            mainGameClass.getScreenHeight() -
                            mainGameClass.getFloorHeight()/2)
