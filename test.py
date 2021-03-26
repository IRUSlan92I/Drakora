import pygame
import random

buttonsPause = (pygame.K_p,)
buttonsQuit = (pygame.K_F10,)
buttonsNewGame = (pygame.K_RETURN,)
buttonsJump = (pygame.K_UP, pygame.K_SPACE,)
buttonsCrouch = (pygame.K_DOWN,)

screenSize = (800, 600)
targetFps = 60

floorHeight = 50

gameSpeed = 0.0
score = 0
isGameOver = False
isPaused = False

isDownJump = False
isDownCrouch = False

enemyCD = 0
enemyChance = 0.0

floors = pygame.sprite.Group()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
player = None

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((screenSize[0], floorHeight))
        self.image.fill((255, 204, 102))
        self.rect = self.image.get_rect()
        self.rect.center = (screenSize[0]/2, screenSize[1]-floorHeight/2)

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((random.randint(150, 350),
                                     random.randint(50, 150)))
        self.image.fill((random.randint(235, 255),
                         random.randint(235, 255),
                         random.randint(235, 255)))
        self.rect = self.image.get_rect()
        self.rect.center = (screenSize[0] + self.rect.width,
                            screenSize[1]/2 -
                                random.randint(100, screenSize[1]/2))
        self.speed = random.randint(10, 30)/10

    def update(self):
        self.rect.x -= gameSpeed*self.speed
        if (self.rect.x < -self.rect.width):
            self.kill()

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

    def crouch(self):
        if not self.isCrouching:
            self.isCrouching = True
            self.rect = self.rect.inflate(0, -25)

    def standup(self):
        if self.isCrouching:
            self.isCrouching = False
            self.rect = self.rect.inflate(0, 25)

    def update(self):
        global isGameOver

        if pygame.sprite.spritecollideany(player, enemies):
            isGameOver = True
            pass

        if not self.speed: self.rect.y += 1

        self.speed += 0.35
        self.rect.y += self.speed

        isOnFloor = False
        while pygame.sprite.spritecollideany(player, floors):
            isOnFloor = True
            self.rect.y -= 1

        if not isDownJump:
            self.hoverCount = 0

        if isOnFloor:
            self.speed = 0

            if isDownJump:
                self.isJumping = True

                if self.isCrouching:
                    self.standup()

            elif isDownCrouch:
                if not self.isCrouching:
                    self.crouch()

            elif self.isCrouching:
                    self.standup()


        if self.isJumping:
            if isDownJump and self.hoverCount < 8:
                self.speed -= 1 - self.speed/8
                self.hoverCount += 1

            else:
                self.isJumping = False



class Enemy(pygame.sprite.Sprite):
    def setNextEnemyType(self):
        if score < 25:
            self.type = 1

        elif score < 50:
            if random.randint(1, 100) < 90: self.type = 1
            else:                           self.type = 2

        else:
            if random.randint(1, 100) < 75: self.type = 1
            else:                           self.type = 2

    def setNextEnemySubtype(self):
        if self.type == 1:
            self.subtype = random.randint(1, 5)
        elif self.type == 2:
            self.subtype = random.randint(1, 3)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.setNextEnemyType()
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
            self.height -= self.rect.height/2 + 10 + 25*self.subtype

        self.rect.center = (screenSize[0] + self.rect.width, self.height)

    def update(self):
        global score, gameSpeed
        self.rect.x -= gameSpeed
        if (self.rect.x < -self.rect.width):
            self.kill()
            score += 1
            gameSpeed += 0.025

def newGame():
    global player, floor, enemies, sprites, score
    global gameSpeed, isGameOver, enemyCD, enemyChance

    for enemy in enemies:
        enemy.kill()

    if player: player.kill()

    player = Player()
    sprites.add(player)

    gameSpeed = 3.0
    score = 0
    isGameOver = False
    isPaused = False

    enemyCD = 0
    enemyChance = 100.0


def init():
    global player, floor, enemies, sprites, score

    random.seed()
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('First test')
    clock = pygame.time.Clock()

    sprites = pygame.sprite.Group()
    floors.add(Floor())
    sprites.add(floors)

    newGame()

    return screen, clock, sprites

def deinit():
    pygame.quit()

def render(screen, sprites):
    screen.fill((102, 153, 255))
    sprites.draw(screen)

    font = pygame.font.Font(pygame.font.match_font('liberation mono'), 12)

    text = font.render('score: %d'%(score), True, (255, 255, 255))
    rect = text.get_rect()
    rect.midtop = (rect.width/2+10,10)
    screen.blit(text, rect)

    text = font.render('game speed: %.1f %s'%\
                (gameSpeed, '(space is pressed)' if isDownJump else ''),
                 True, (255, 255, 255))
    rect = text.get_rect()
    rect.midtop = (rect.width/2+10,25)
    screen.blit(text, rect)

    text = font.render('player speed: %.1f'%(player.speed),
                       True, (255, 255, 255))
    rect = text.get_rect()
    rect.midtop = (rect.width/2+10,40)
    screen.blit(text, rect)

    text = font.render('enemy CD: %.1f'%(enemyCD), True, (255, 255, 255))
    rect = text.get_rect()
    rect.midtop = (rect.width/2+10,55)
    screen.blit(text, rect)

    text = font.render('enemy chance: %.1f'%(enemyChance),
                       True, (255, 255, 255))
    rect = text.get_rect()
    rect.midtop = (rect.width/2+10,70)
    screen.blit(text, rect)

    if isGameOver:
        font = pygame.font.Font(pygame.font.match_font('liberation mono'), 56)
        text = font.render('GAME OVER', True, (255, 255, 255))
        rect = text.get_rect()
        rect.midtop = tuple(i/2 for i in screenSize)
        screen.blit(text, rect)
    elif isPaused:
        font = pygame.font.Font(pygame.font.match_font('liberation mono'), 56)
        text = font.render('PAUSED', True, (255, 255, 255))
        rect = text.get_rect()
        rect.midtop = tuple(i/2 for i in screenSize)
        screen.blit(text, rect)


    pygame.display.flip()


def logic(clock, sprites):
    global enemyCD, enemyChance, isDownJump, isDownCrouch, isPaused

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            if event.key in buttonsQuit:
                return False
            if event.key in buttonsCrouch:
                isDownCrouch = True
            elif event.key in buttonsJump:
                isDownJump = True
            elif event.key in buttonsNewGame:
                if isGameOver: newGame()
            elif event.key in buttonsPause:
                isPaused = not isPaused

        elif event.type == pygame.KEYUP:
            if event.key in buttonsCrouch:
                isDownCrouch = False
            if event.key in buttonsJump:
                isDownJump = False

    if not isGameOver and not isPaused:
        sprites.update()

        enemyCD -= gameSpeed

        if random.randint(1, 100) == 1:
            cloud = Cloud()
            clouds.add(cloud)
            sprites.add(cloud)

        if enemyCD <= 0:
            enemyChance += (1/targetFps) * enemyChance/8

            if random.randint(1, 100) < enemyChance:
                enemyCD = 300
                enemyChance = 1
                enemy = Enemy()
                enemies.add(enemy)
                sprites.add(enemy)


    clock.tick(targetFps)

    return True

def main_loop(screen, clock, sprites):
    global isGameOver

    isRunning = True

    while isRunning:
        isRunning = logic(clock, sprites)
        render(screen, sprites)

if __name__ == '__main__':
    screen, clock, sprites = init()
    main_loop(screen, clock, sprites)
    deinit()
