"""
Player entity class
"""


import pygame
import math
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.imgDir = os.path.join(os.path.dirname(__file__), 'data')

        playerImage = pygame.image.load(os.path.join(self.imgDir, 'player.png')).convert()

        self.walkImages = (
            pygame.transform.scale(playerImage.subsurface((0, 0, 16, 24)), (64, 98)),
            pygame.transform.scale(playerImage.subsurface((16, 0, 16, 24)), (64, 98)),
            pygame.transform.scale(playerImage.subsurface((32, 0, 16, 24)), (64, 98)),
            pygame.transform.scale(playerImage.subsurface((16, 0, 16, 24)), (64, 98)),
        )
        self.currentWalkImage = 0

        self.upImages = (
            pygame.transform.scale(playerImage.subsurface((0, 24, 16, 24)), (64, 98)),
            pygame.transform.scale(playerImage.subsurface((16, 24, 16, 24)), (64, 98)),
            pygame.transform.scale(playerImage.subsurface((32, 24, 16, 24)), (64, 98)),
        )
        self.currentUpImage = 0

        self.downImages = (
            pygame.transform.scale(playerImage.subsurface((0, 48, 16, 24)), (64, 98)),
            pygame.transform.scale(playerImage.subsurface((16, 48, 16, 24)), (64, 98)),
            pygame.transform.scale(playerImage.subsurface((32, 48, 16, 24)), (64, 98)),
        )
        self.currentDownImage = 0

        self.crouchImages = (
            pygame.transform.scale(playerImage.subsurface((0, 72, 16, 16)), (64, 64)),
            pygame.transform.scale(playerImage.subsurface((16, 72, 16, 16)), (64, 64)),
        )
        self.currentCrouchImage = 0

        for array in (self.walkImages, self.upImages, self.downImages, self.crouchImages):
            for image in array:
                image.set_colorkey((255,0,255))

        pygame.sprite.Sprite.__init__(self)
        self.image = self.walkImages[self.currentWalkImage]

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
        self.gameSpeed = 1
        self.updateCount = 0


    def crouch(self):
        if not self.isCrouching:
            self.isCrouching = True
            self.rect = self.rect.inflate(0, -32)


    def standup(self):
        if self.isCrouching:
            self.isCrouching = False
            self.rect = self.rect.inflate(0, 32)

    def updateSpeed(self, newGameSpeed):
        self.gameSpeed = newGameSpeed

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
        if not self.speed: self.rect.y += 1

        if not self.isDownJump:
            self.hoverCount = 0

        if self.isOnFloor:
            self.speed = 0

            if self.isDownJump:
                self.isJumping = True

                if self.isCrouching:
                    self.standup()

            elif self.isDownCrouch:
                if not self.isCrouching:
                    self.crouch()

            elif self.isCrouching:
                    self.standup()

        if self.isJumping:
            if self.gameSpeed <= 2:     maxHoverCount = 30
            elif self.gameSpeed <= 4:   maxHoverCount = 23
            elif self.gameSpeed <= 8:   maxHoverCount = 16
            elif self.gameSpeed <= 16:  maxHoverCount = 9
            elif self.gameSpeed <= 32:  maxHoverCount = 5
            elif self.gameSpeed <= 64:  maxHoverCount = 2
            else:                       maxHoverCount = 1

            if self.isDownJump and self.hoverCount < maxHoverCount:
                self.speed -= self.gameSpeed/8 * ((math.cos(2*math.pi*self.hoverCount/(2*maxHoverCount))+1)/2.5+0.2)
                self.hoverCount += 1
            else:
                self.isJumping = False
        else:
            self.speed += 0.07 * self.gameSpeed

        self.rect.y += self.speed

        self.updateCount += 1
        if self.updateCount == 22 - math.log2(self.gameSpeed) * 2:
            if self.isOnFloor:
                if self.isCrouching:
                    self.currentCrouchImage += 1
                    if self.currentCrouchImage >= len(self.crouchImages):
                        self.currentCrouchImage = 0
                    self.image = self.crouchImages[self.currentCrouchImage]
                else:
                    self.currentWalkImage += 1
                    if self.currentWalkImage >= len(self.walkImages):
                        self.currentWalkImage = 0
                    self.image = self.walkImages[self.currentWalkImage]
            elif self.isJumping:
                self.currentUpImage += 1
                if self.currentUpImage >= len(self.upImages):
                    self.currentUpImage = 0
                self.image = self.upImages[self.currentUpImage]
            else:
                self.currentDownImage += 1
                if self.currentDownImage >= len(self.downImages):
                    self.currentDownImage = 0
                self.image = self.downImages[self.currentDownImage]
            self.updateCount = 0
