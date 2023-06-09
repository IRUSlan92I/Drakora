"""
Cloud entity class
"""


import pygame
import random
import os


class Cloud(pygame.sprite.Sprite):
    imgDir = os.path.join(os.path.dirname(__file__), 'data')
    cloudImage = pygame.image.load(
        os.path.join(imgDir, 'cloud.png')
    )#.convert()
    images = (
        pygame.transform.scale(
            cloudImage.subsurface((0, 0, 128, 32)), (512, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((128, 0, 128, 32)), (512, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((256, 0, 128, 32)), (512, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((0, 32, 128, 32)), (512, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((128, 32, 128, 32)), (512, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((256, 32, 128, 32)), (512, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((0, 64, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((96, 64, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((192, 64, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((288, 64, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((0, 96, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((96, 96, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((192, 96, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((288, 96, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((0, 128, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((96, 128, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((192, 128, 96, 32)), (384, 128)
        ),
        pygame.transform.scale(
            cloudImage.subsurface((288, 128, 96, 32)), (384, 128)
        ),
    )
    for image in images:
        image.set_colorkey((255,0,255))

    def __init__(self, mainGameClass, cloudType):
        pygame.sprite.Sprite.__init__(self)

        self.type = cloudType
        self.mainGameClass = mainGameClass

        self.image = Cloud.images[random.randint(0, len(Cloud.images)-1)]

        # self.image = pygame.Surface((random.randint(128, 512),
        #                              random.randint(32, 128)))

        # color = 255 - 15 * (3-cloudType)
        # self.image.fill((color, color, color))

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
