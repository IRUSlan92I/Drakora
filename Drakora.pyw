"""
First test Pygame project

Written in Python 3.X using Pygame library
"""


import pygame
import random


class Floor(pygame.sprite.Sprite):
    def __init__(self, screenSize, floorHeight):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((screenSize[0], floorHeight))
        self.image.fill((255, 204, 102))
        self.rect = self.image.get_rect()
        self.rect.center = (screenSize[0]/2, screenSize[1]-floorHeight/2)


class Cloud(pygame.sprite.Sprite):
    def __init__(self, screenSize, gameSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((random.randint(150, 350),
                                     random.randint(50, 150)))
        self.image.fill((random.randint(235, 255),
                         random.randint(235, 255),
                         random.randint(235, 255)))
        self.rect = self.image.get_rect()
        self.rect.center = (screenSize[0] + self.rect.width,
                            screenSize[1]/2 -
                                random.randint(100, screenSize[1]/2-100))
        self.speed = random.randint(150, 300)/100*gameSpeed


    def update(self):
        self.rect.x -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 75))
        self.image.fill((153, 151, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 400)
        self.speed = 0.0
        self.isJumping = False
        self.isCrouching = False
        self.hoverCount = 0
        self.isOnFloor = False


    def crouch(self):
        if not self.isCrouching:
            self.isCrouching = True
            self.rect = self.rect.inflate(0, -25)


    def standup(self):
        if self.isCrouching:
            self.isCrouching = False
            self.rect = self.rect.inflate(0, 25)


    def update(self):
        if not self.speed: self.rect.y += 1

        self.speed += 0.35
        self.rect.y += self.speed


class Enemy(pygame.sprite.Sprite):
    def setNextEnemyType(self, score):
        if score < 10:
            self.type = 1

        elif score < 25:
            if random.randint(1, 100) < 95: self.type = 1
            else:                           self.type = 2

        elif score < 50:
            if random.randint(1, 100) < 85: self.type = 1
            else:                           self.type = 2

        else:
            if random.randint(1, 100) < 75: self.type = 1
            else:                           self.type = 2


    def setNextEnemySubtype(self):
        if self.type == 1:
            self.subtype = random.randint(1, 5)
        elif self.type == 2:
            self.subtype = random.randint(1, 7)


    def __init__(self, screenSize, floorHeight, gameSpeed, score):
        pygame.sprite.Sprite.__init__(self)

        self.speed = gameSpeed

        self.setNextEnemyType(score)
        self.setNextEnemySubtype()

        self.height = screenSize[1] - floorHeight

        if self.type == 1:
            if self.subtype == 1:   self.image = pygame.Surface((25, 75))
            elif self.subtype == 2: self.image = pygame.Surface((25, 25))
            elif self.subtype == 3: self.image = pygame.Surface((75, 25))
            elif self.subtype == 4: self.image = pygame.Surface((50, 25))
            elif self.subtype == 5: self.image = pygame.Surface((50, 50))
            else:                   self.image = pygame.Surface((25, 50))

            self.image.fill((0, 153, 0))
            self.rect = self.image.get_rect()
            self.height -= self.rect.height/2

        elif self.type == 2:
            self.image = pygame.Surface((50, 25))
            self.image.fill((51, 51, 0))
            self.rect = self.image.get_rect()
            self.height -= self.rect.height/2 + 10 + 10*self.subtype

        self.rect.center = (screenSize[0] + self.rect.width, self.height)


    def update(self):
        if self.type == 1:
            self.rect.x -= self.speed
        else:
            self.rect.x -= self.speed*2


class Drakora():
    def newGame(self):
        for enemy in self.enemies:
            enemy.kill()

        if self.player: self.player.kill()

        self.player = Player()
        self.sprites.add(self.player)

        self.score = 0
        self.isGameOver = False
        self.isPaused = False

        self.gameSpeed = 3

        self.enemyCD = 0
        self.enemyChance = 100.0


    def __init__(self):
        self.buttonsPause = (pygame.K_p,)
        self.buttonsQuit = (pygame.K_F10,)
        self.buttonsNewGame = (pygame.K_RETURN,)
        self.buttonsJump = (pygame.K_UP, pygame.K_SPACE,)
        self.buttonsCrouch = (pygame.K_DOWN,)

        self.screenSize = (800, 600)
        self.targetFps = 60

        self.floorHeight = 50

        self.isDownJump = False
        self.isDownCrouch = False

        self.floors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.player = None

        random.seed()
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption('Drakora')
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()
        self.floors.add(Floor(self.screenSize, self.floorHeight))
        self.sprites.add(self.floors)

        font = pygame.font.match_font('liberation mono')
        self.fontScore = pygame.font.Font(font, 32)
        self.fontMessage = pygame.font.Font(font, 56)

        self.newGame()


    def __del__(self):
        pygame.quit()


    def renderText(self, text, font, color, center):
        render = font.render(text, True, color)
        rect = render.get_rect()
        rect.center = center
        self.screen.blit(render, rect)


    def render(self):
        self.screen.fill((102, 153, 255))
        self.sprites.draw(self.screen)

        self.renderText('%d'%(self.score),
                        self.fontScore, (255, 255, 255),
                         (self.screenSize[0]/2,20))

        if self.isGameOver:
            self.renderText('GAME OVER',
                            self.fontMessage, (255, 255, 255),
                            tuple(i/2 for i in self.screenSize))
        elif self.isPaused:
            self.renderText('PAUSED',
                            self.fontMessage, (255, 255, 255),
                            tuple(i/2 for i in self.screenSize))

        pygame.display.flip()


    def collideCheck(self):
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.isGameOver = True

        for enemy in self.enemies:
            if (enemy.rect.x < -enemy.rect.width):
                enemy.kill()
                self.score += 1
                self.gameSpeed += 0.025
                """Quick fix of running cacti. Some good fix needed"""
                for enemy in self.enemies: enemy.speed = self.gameSpeed

        for cloud in self.clouds:
            if (cloud.rect.x < -cloud.rect.width):
                cloud.kill()

        self.player.isOnFloor = False
        while pygame.sprite.spritecollideany(self.player, self.floors):
            self.player.isOnFloor = True
            self.player.rect.y -= 1

        if not self.isDownJump:
            self.player.hoverCount = 0

        if self.player.isOnFloor:
            self.player.speed = 0

            if self.isDownJump:
                self.player.isJumping = True

                if self.player.isCrouching:
                    self.player.standup()

            elif self.isDownCrouch:
                if not self.player.isCrouching:
                    self.player.crouch()

            elif self.player.isCrouching:
                    self.player.standup()

        if self.player.isJumping:
            if self.isDownJump and self.player.hoverCount < 10:
                self.player.speed -= 1 - self.player.speed/(15+
                                              self.player.hoverCount*3)
                self.player.hoverCount += 1

            else:
                self.player.isJumping = False


    def logic(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key in self.buttonsQuit:
                    return False
                if event.key in self.buttonsCrouch:
                    self.isDownCrouch = True
                elif event.key in self.buttonsJump:
                    self.isDownJump = True
                elif event.key in self.buttonsNewGame:
                    if self.isGameOver: self.newGame()
                elif event.key in self.buttonsPause:
                    self.isPaused = not self.isPaused

            elif event.type == pygame.KEYUP:
                if event.key in self.buttonsCrouch:
                    self.isDownCrouch = False
                if event.key in self.buttonsJump:
                    self.isDownJump = False

        if not self.isGameOver and not self.isPaused:
            self.sprites.update()

            self.enemyCD -= self.gameSpeed

            if random.randint(1, 100) == 1:
                cloud = Cloud(self.screenSize, self.gameSpeed)
                self.clouds.add(cloud)
                self.sprites.add(cloud)

            if self.enemyCD <= 0:
                self.enemyChance += (1/self.targetFps) * self.enemyChance/8

                if random.randint(1, 100) < self.enemyChance:
                    self.enemyCD = 200
                    self.enemyChance = 1
                    enemy = Enemy(self.screenSize, self.floorHeight,
                                  self.gameSpeed, self.score)
                    self.enemies.add(enemy)
                    self.sprites.add(enemy)

        self.collideCheck()

        self.clock.tick(self.targetFps)

        return True


    def play(self):
        isRunning = True

        while isRunning:
            isRunning = self.logic()
            self.render()


if __name__ == '__main__':
    drakora = Drakora()
    drakora.play()
    del Drakora
