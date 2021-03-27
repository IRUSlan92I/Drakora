"""
Cloud entity class
"""


import pygame
import random


class Cloud(pygame.sprite.Sprite):
    def __init__(self, mainGameClass):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((random.randint(150, 350),
                                     random.randint(50, 150)))
        self.image.fill((random.randint(235, 255),
                         random.randint(235, 255),
                         random.randint(235, 255)))
        self.rect = self.image.get_rect()
        self.rect.center = (mainGameClass.getScreenWidth() + self.rect.width,
                            mainGameClass.getScreenHeight()/2 -
                            random.randint(100,
                                mainGameClass.getScreenHeight()/2-100))
        self.speed = random.randint(2, 4)*mainGameClass.getGameSpeed()


    def update(self):
        if (self.rect.x < -self.rect.width):
            self.kill()

        self.rect.x -= self.speed
