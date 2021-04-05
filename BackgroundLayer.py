"""
Background layer entity class
"""


import pygame

from BackgroundLayerFrame import BackgroundLayerFrame


class BackgroundLayer():
    def __init__(self, image, mainGameClass, speedMultiplier):
        offset = image.get_width()

        self.frames = pygame.sprite.Group()

        self.frames.add(BackgroundLayerFrame(image, mainGameClass, (0, 0), speedMultiplier))
        self.frames.add(BackgroundLayerFrame(image, mainGameClass, (offset, 0), speedMultiplier))


    def update(self):
        for frame in self.frames:
            frame.update()


    def draw(self, surface):
        self.frames.draw(surface)
