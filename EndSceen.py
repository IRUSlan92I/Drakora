"""
Endscreen class
"""


import pygame


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

        self.game = mainGameClass
        self.saveFileName = 'leaders.lb'

        self.maxNumberNameLetters = 13
        self.fstr = ' {0:3d} {1:^'+str(self.maxNumberNameLetters)+'} {2:6d} {3:8.2f} ';


    def getScorePosition(self, score):
        counter = 1
        for i in self.sortedDataByScores:
            if i[1][1] < score:
                return counter
            else:
                counter += 1
        return counter


    def newEndScreen(self):
        self.endScreenTimer = 0;
        self.playerName = 'Player'

        self.scoresFromFile = []
        self.data = []
        self.sortedDataByScores = []

        self.isBackButton = True

        self.data = self.getResultsFromFile()
        self.sortedDataByScores = sorted(enumerate(self.data),
                                        key=lambda i: i[1][1], reverse=True)


    def getResultsFromFile(self):
        data = []

        try:
            with open(self.saveFileName, 'rb') as file:
                fileData = self.shiftRight(file.read()).decode('utf-8')
                for line in fileData.split('\n'):
                        name, score, time = line.split('\t')
                        data.append(
                            [name[:self.maxNumberNameLetters], int(score), float(time)]
                        )
        except Exception:
            pass

        return data


    def saveResults(self):
        data = self.getResultsFromFile()

        data.append(
            [self.playerName[:self.maxNumberNameLetters],
            int(self.game.getScore()),
            float(self.game.getTime())]
        )

        try:
            with open(self.saveFileName, 'wb') as file:
                for entry in data:
                    string = '{}\t{}\t{}\n'.format(*entry)
                    arr = string.encode('utf-8')
                    file.write(self.shiftLeft(arr))
        except Exception:
            pass


    def shift(self, c, offset):
        return (c + offset)%0x100


    def shiftLeft(self, arr):
        return bytearray([self.shift(x, -77) for x in arr])


    def shiftRight(self, arr):
        return bytearray([self.shift(x, +77) for x in arr])


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
                self.renderText(('>'+self.fstr).format(j,
                                    self.playerName[:self.maxNumberNameLetters], self.game.getScore(),
                                    self.game.getTime()
                                ),
                                self.fontLeaderBoard, (255, 255, 255),
                                (self.game.getScreenWidth()/2,100 + j*50))
                j += 1
                placeFlag = True

            if (j > number):
                break

            formatDataForOnePlayer = (' '+self.fstr).format(
                                                            j, *self.data[i])

            self.renderText(formatDataForOnePlayer,
                            self.fontLeaderBoard, (255, 255, 255),
                            (self.game.getScreenWidth()/2,100 + j*50))

            j += 1

            if (j > number):
                break

        if not placeFlag and j <= number:
            self.renderText(('>'+self.fstr).format(
                                j, self.playerName[:self.maxNumberNameLetters], self.game.getScore(),
                                self.game.getTime()
                            ),
                            self.fontLeaderBoard, (255, 255, 255),
                            (self.game.getScreenWidth()/2,100 + j*50))

        tmpStr = '  {0:>3} {1:^'+str(self.maxNumberNameLetters)+'} {2:>6} {3:>8} '
        self.renderText(tmpStr.format(
                            '..','.....', '..', '.....'
                        ),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100 + (number + 1)*50))


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
            self.renderText((' '+self.fstr).format(
                            self.getScorePosition(self.game.getScore()),
                            self.playerName[:self.maxNumberNameLetters] + (cursorChar
                                if len(self.playerName) < self.maxNumberNameLetters else ''),
                            self.game.getScore(), self.game.getTime()
                        ),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100 + (5 + 2)*50))
        else:
            self.renderText((' '+self.fstr).format(
                            self.getScorePosition(self.game.getScore()),
                            self.playerName[:self.maxNumberNameLetters] + (cursorChar
                                if len(self.playerName) < self.maxNumberNameLetters else ''),
                            self.game.getScore(), self.game.getTime()
                        ),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2, 100 +
                            (5 + 2)*50), (208, 85, 52))

            tmpStr = '{0:^'+str(len(self.fstr))+'}'
            self.renderText(tmpStr.format('Missing player name'),
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
            ) == 1 and len(self.playerName) < self.maxNumberNameLetters:
                if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    self.playerName += pygame.key.name(event.key).upper()
                else:
                    self.playerName += pygame.key.name(event.key).lower()
