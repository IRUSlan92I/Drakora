"""
CollisionBox entity class
"""

import pygame


class CollisionBox(pygame.sprite.Sprite):
    def __init__(self, offsetX, offsetY, width, height, center):
        pygame.sprite.Sprite.__init__(self)

        self.offset = (offsetX, offsetY)
        self.size = (width, height)
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center

        self.rect.x += self.offset[0]
        self.rect.y += self.offset[1]


    def setY(self, y):
        self.rect.y = y + self.offset[1]


    def setX(self, x):
        self.rect.x = x + self.offset[0]
