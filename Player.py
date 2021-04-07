"""
Player entity class
"""


import pygame
import math
import os
from CollisionBox import CollisionBox


class Player(pygame.sprite.Sprite):
    imgDir = os.path.join(os.path.dirname(__file__), 'data')
    playerImage = pygame.image.load(
        os.path.join(imgDir, 'player.png')
    )#.convert()
    walkImages = (
        pygame.transform.scale(
            playerImage.subsurface((0, 0, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((16, 0, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((32, 0, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((48, 0, 16, 24)), (64, 98)
        ),
    )

    upImages = (
        pygame.transform.scale(
            playerImage.subsurface((0, 24, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((16, 24, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((32, 24, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((48, 24, 16, 24)), (64, 98)
        ),
    )

    downImages = (
        pygame.transform.scale(
            playerImage.subsurface((0, 48, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((16, 48, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((32, 48, 16, 24)), (64, 98)
        ),
        pygame.transform.scale(
            playerImage.subsurface((48, 48, 16, 24)), (64, 98)
        ),
    )

    crouchImages = (
        pygame.transform.scale(
            playerImage.subsurface((0, 72, 16, 16)), (64, 64)
        ),
        pygame.transform.scale(
            playerImage.subsurface((16, 72, 16, 16)), (64, 64)
        ),
        pygame.transform.scale(
            playerImage.subsurface((32, 72, 16, 16)), (64, 64)
        ),
        pygame.transform.scale(
            playerImage.subsurface((48, 72, 16, 16)), (64, 64)
        ),
    )

    for array in (walkImages, upImages, downImages, crouchImages):
        for image in array:
            image.set_colorkey((255,0,255))


    def __init__(self, mainGameClass):
        pygame.sprite.Sprite.__init__(self)

        self.mainGameClass = mainGameClass

        self.currentWalkImage = 0
        self.currentUpImage = 0
        self.currentDownImage = 0
        self.currentCrouchImage = 0

        self.image = Player.downImages[self.currentDownImage]

        self.rect = self.image.get_rect()
        self.rect.center = (100, 400)
        self.speed = 0.0
        self.isJumping = False
        self.isCrouching = False
        self.hoverCount = 0
        self.isOnFloor = False
        self.isDownJump = False
        self.isDownCrouch = False
        self.buttonsJump = (pygame.K_UP, pygame.K_SPACE,)
        self.buttonsCrouch = (pygame.K_DOWN,)
        self.updateCount = 0

        self.collisionBoxes = pygame.sprite.Group()

        self.collisionBoxes.add(CollisionBox(0, 20, 60, 20, self.rect.center))
        self.collisionBoxes.add(CollisionBox(-10, 5, 30, 20, self.rect.center))
        self.collisionBoxes.add(CollisionBox(0, 35, 25, 40, self.rect.center))

        self.__doubleY = float(self.rect.y)


    def getCollisionBoxes(self):
        return self.collisionBoxes


    def crouch(self):
        if not self.isCrouching:
            self.isCrouching = True
            self.rect = self.rect.inflate(0, -32)


    def standup(self):
        if self.isCrouching:
            self.isCrouching = False
            self.rect = self.rect.inflate(0, 32)


    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.buttonsCrouch:
                self.isDownCrouch = True
            elif event.key in self.buttonsJump:
                self.isDownJump = True

        elif event.type == pygame.KEYUP:
            if event.key in self.buttonsCrouch:
                self.isDownCrouch = False
            elif event.key in self.buttonsJump:
                self.isDownJump = False


    def update(self):
        self.updateCount += 1

        if not self.isDownJump:
            self.hoverCount = 0

        if self.isOnFloor:
            self.speed = 0.0

            if self.isDownJump:
                self.isJumping = True

                if self.isCrouching:
                    self.standup()

            elif self.isDownCrouch:
                if not self.isCrouching:
                    self.crouch()

            elif self.isCrouching:
                    self.standup()

        gameSpeed = self.mainGameClass.getGameSpeed()

        if self.isJumping:
            if gameSpeed <= 2:     maxHoverCount = 40
            elif gameSpeed <= 4:   maxHoverCount = 29
            elif gameSpeed <= 8:   maxHoverCount = 20
            elif gameSpeed <= 16:  maxHoverCount = 9
            elif gameSpeed <= 32:  maxHoverCount = 5
            elif gameSpeed <= 64:  maxHoverCount = 2
            else:                  maxHoverCount = 1

            if self.isDownJump and self.hoverCount < maxHoverCount:
                self.speed -= gameSpeed/8 * (
                    (math.cos(2*math.pi*self.hoverCount/(2*maxHoverCount))
                     + 1)/2.5 + 0.2
                )
                self.hoverCount += 1
            else:
                self.isJumping = False
        else:
            self.speed += 0.07 * gameSpeed

        self.__doubleY += self.speed
        self.rect.y = self.__doubleY

        for collisionBox in self.collisionBoxes:
            collisionBox.setY(self.rect.y)

        if self.updateCount >= 22 - math.log2(gameSpeed) * 2:
            if self.isOnFloor:
                if self.isCrouching:
                    self.currentCrouchImage += 1
                    if self.currentCrouchImage >= len(Player.crouchImages):
                        self.currentCrouchImage = 0
                    self.image = Player.crouchImages[self.currentCrouchImage]
                else:
                    self.currentWalkImage += 1
                    if self.currentWalkImage >= len(Player.walkImages):
                        self.currentWalkImage = 0
                    self.image = Player.walkImages[self.currentWalkImage]
            elif self.isJumping:
                self.currentUpImage += 1
                if self.currentUpImage >= len(Player.upImages):
                    self.currentUpImage = 0
                self.image = Player.upImages[self.currentUpImage]
            else:
                self.currentDownImage += 1
                if self.currentDownImage >= len(Player.downImages):
                    self.currentDownImage = 0
                self.image = Player.downImages[self.currentDownImage]
            self.updateCount = 0
