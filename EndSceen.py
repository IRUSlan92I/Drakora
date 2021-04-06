"""
Enemy entity class
"""

import pickle
import pygame
import hashlib
from cryptography.fernet import Fernet


class EndSceen():
    def __init__(self, mainGameClass):
        self.fontGameOver = pygame.font.Font(
            mainGameClass.getFont(), 56
        )
        self.fontLeaderBoard = pygame.font.Font(
            mainGameClass.getFont(), 30
        )
        self.fontLeaderBoardActive = pygame.font.Font(
            mainGameClass.getFont(), 30
        )
        self.fontLeaderBoardActive.underline = True
        self.fontError = pygame.font.Font(
            mainGameClass.getFont(), 15
        )

        key = b'Lh2b2rragfwD8QR4VU-V2TmSuio4yp-WbFwo4tcoyzs='
        self.code = Fernet(key)

        self.game = mainGameClass
        self.saveFileName = 'leaders.lb'

    def newEndScreen(self):
        self.endScreenTimer = 0;
        self.playerName = 'Player'

        self.scoresFromFile = []
        self.data = []
        self.sortedDataByScores = []

        self.isBackButton = True

        try:
            fileWithData = open(self.saveFileName, 'rb')
        except IOError as e:
            pass
        else:
            listPlayers = pickle.load(fileWithData)

            for line in listPlayers:
                oneStr = self.code.decrypt(line).decode().split()

                if (len(oneStr) == 3):
                    self.data.append(
                        [oneStr[0][:10], int(oneStr[1]), float(oneStr[2])]
                    )

            fileWithData.close()

            self.sortedDataByScores = sorted(enumerate(self.data),
                                            key=lambda i: i[1][1], reverse=True)


    def renderText(self, text, font, color, center, backColor=None):
        render = font.render(text, True, color, backColor)
        rect = render.get_rect()
        rect.center = center
        self.game.screen.blit(render, rect)

    def drawTableLB(self, number):
        j = 1
        placeFlag = False

        for i in [i[0] for i in self.sortedDataByScores[:number]]:
            if (self.game.getScore() > self.data[i][1] and not placeFlag):
                self.renderText('>{0:3} {1:^10} {2:6d} {3:8.2f} '.format(j,
                                    self.playerName[:10], self.game.getScore(),
                                    self.game.getTime()
                                ),
                                self.fontLeaderBoard, (255, 255, 255),
                                (self.game.getScreenWidth()/2,100 + j*50))
                j += 1
                placeFlag = True

            if (j > number):
                break

            formatDataForOnePlayer = ' {0:3} {1:^10} {2:6d} {3:8.2f} '.format(
                                                            j, *self.data[i])

            self.renderText(formatDataForOnePlayer,
                            self.fontLeaderBoard, (255, 255, 255),
                            (self.game.getScreenWidth()/2,100 + j*50))

            j += 1

            if (j > number):
                break

        if not placeFlag and j <= number:
            self.renderText('>{0:3} {1:^10} {2:6d} {3:8.2f} '.format(
                                j, self.playerName[:10], self.game.getScore(),
                                self.game.getTime()
                            ),
                            self.fontLeaderBoard, (255, 255, 255),
                            (self.game.getScreenWidth()/2,100 + j*50))


        self.renderText(' {0:>3} {1:^10} {2:>6} {3:>8} '.format(
                            '..','.....', '..', '.....'
                        ),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100 + (number + 1)*50))

    def getScorePosition(self, score):
        counter = 1
        for i in self.sortedDataByScores:
            if i[1][1] < score:
                return counter
            else:
                counter += 1
        return counter


    def render(self):
        backGround = pygame.Surface(self.game.screenSize, pygame.SRCALPHA)
        backGround.fill((0,0,0,200))
        self.game.screen.blit(backGround, (0,0))

        self.renderText('GAME OVER',
                        self.fontGameOver, (255, 255, 255),
                        (self.game.getScreenWidth()/2,50))

        self.renderText('Leaderboard',
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100))

        self.drawTableLB(5)

        cursorChar = ' '
        if self.endScreenTimer > self.game.targetFps / 3:
            cursorChar = '_'

        if self.endScreenTimer > 2 * self.game.targetFps / 3:
            self.endScreenTimer = 0

        self.endScreenTimer += 1

        if len(self.playerName) > 0:
            self.renderText(' {0:3d} {1:^10} {2:6d} {3:8.2f} '.format(
                            self.getScorePosition(self.game.getScore()),
                            self.playerName[:10] + (cursorChar
                                if len(self.playerName) < 10 else ''),
                            self.game.getScore(), self.game.getTime()
                        ),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100 + (5 + 2)*50))
        else:
            self.renderText(' {0:3d} {1:^10} {2:6d} {3:8.2f} '.format(
                            self.getScorePosition(self.game.getScore()),
                            self.playerName[:10] + (cursorChar
                                if len(self.playerName) < 10 else ''),
                            self.game.getScore(), self.game.getTime()
                        ),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2, 100 +
                            (5 + 2)*50), (200, 20, 20))

            self.renderText(' {0:^30} '.format('Missing player name'),
                        self.fontError, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100 + (5 + 2)*50 + 25))

        self.renderText('Back',
                        self.fontLeaderBoard if not self.isBackButton else
                            self.fontLeaderBoardActive, (255, 255, 255),
                        (self.game.getScreenWidth()/2 - 100,
                            self.game.getScreenHeight() - 80))

        self.renderText('Continue',
                        self.fontLeaderBoard if self.isBackButton else
                            self.fontLeaderBoardActive, (255, 255, 255),
                        (self.game.getScreenWidth()/2 + 100,
                            self.game.getScreenHeight() - 80))

    def control(self, event):
        if event.type == pygame.KEYDOWN and self.game.isGameOver:
            if event.key == pygame.K_RIGHT:
                self.isBackButton = False

            elif event.key == pygame.K_LEFT:
                self.isBackButton = True

            elif event.key == pygame.K_RETURN:
                if len(self.playerName) > 0:
                    self.saveResults()

                    if self.isBackButton:
                        self.game.newGame()
                    else:
                        self.game.newGame()

            elif event.key == pygame.K_BACKSPACE:
                self.playerName = self.playerName[:len(self.playerName) - 1]

            elif len(
                pygame.key.name(event.key)
            ) == 1 and len(self.playerName) < 10:
                if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    self.playerName += pygame.key.name(event.key).upper()
                else:
                    self.playerName += pygame.key.name(event.key).lower()

    def saveResults(self):
        newData = []

        try:
            fileWithData = open(self.saveFileName, 'rb')
        except IOError as e:
            pass
        else:
            tmpData = pickle.load(fileWithData)
            fileWithData.close()

            for line in tmpData:
                oneStr = self.code.decrypt(line).decode()
                if len(oneStr.split()) == 3:
                    if not (oneStr.split()[0].rstrip() == self.playerName.rstrip()):
                        newData.append(line)

        newData.append(self.code.encrypt(('{0} {1} {2:.2f}\n'.format(self.playerName,
                        self.game.getScore(), self.game.getTime())).encode()))

        with open (self.saveFileName, 'wb') as fileWithData:
            pickle.dump(newData, fileWithData)
        fileWithData.close()
