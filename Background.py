"""
Background entity class
"""


import pygame
import os

from BackgroundLayer import BackgroundLayer


class Background():
    imgDir = os.path.join(os.path.dirname(__file__), 'data')
    backgroundImage = pygame.image.load(os.path.join(imgDir, 'background.png'))#.convert()
    backgroundImages = (
        pygame.transform.scale(backgroundImage.subsurface((0, 0, 800, 150)), (3200, 600)),
        pygame.transform.scale(backgroundImage.subsurface((0, 150, 800, 150)), (3200, 600)),
        pygame.transform.scale(backgroundImage.subsurface((0, 300, 800, 150)), (3200, 600)),
    )
    for image in backgroundImages:
        image.set_colorkey((255,0,255))

    def __init__(self, mainGameClass):
        pygame.sprite.Sprite.__init__(self)

        self.layers = (
            BackgroundLayer(Background.backgroundImages[0], mainGameClass, 0.25),
            BackgroundLayer(Background.backgroundImages[1], mainGameClass, 0.5),
            BackgroundLayer(Background.backgroundImages[2], mainGameClass, 1),
        )


    def update(self):
        for layer in self.layers:
            layer.update()


    def draw(self, surface):
        for layer in self.layers:
            layer.draw(surface)
