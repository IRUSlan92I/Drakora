"""
Enemy entity class
"""


import pygame


class EndSceen():
    def __init__(self, mainGameClass):
        self.fontGameOver = pygame.font.Font(mainGameClass.getFont(), 56)
        self.fontLeaderBoard = pygame.font.Font(mainGameClass.getFont(), 30)
        self.fontLeaderBoardActive = pygame.font.Font(mainGameClass.getFont(), 30)
        self.fontLeaderBoardActive.underline = True
        self.game = mainGameClass

    def newEndScreen(self):
        self.playerName = 'Player'

        self.scoresFromFile = []
        self.data = []

        self.isBackButton = True

        fileWithData = open('leaders.txt')

        for line in fileWithData:
            oneStr = line.split()

            if (len(oneStr) == 3):
                self.data.append([oneStr[0][:10], int(oneStr[1]), float(oneStr[2])])

        fileWithData.close()

        self.sortedDataByScores = sorted(enumerate(self.data), key=lambda i: i[1][1], reverse=True)


    def renderText(self, text, font, color, center):
        render = font.render(text, True, color)
        rect = render.get_rect()
        rect.center = center
        self.game.screen.blit(render, rect)

    def drawTableLB(self, number):
        j = 1
        placeFlag = False

        for i in [i[0] for i in self.sortedDataByScores[:number]]:
            # print(self.data[i])

            if (self.game.getScore() > self.data[i][1] and not placeFlag):
                self.renderText('>{0:3} {1:^10} {2:6d} {3:8.2f}'.format(j, self.playerName[:10], self.game.getScore(), self.game.getTime()),
                                self.fontLeaderBoard, (255, 255, 255),
                                (self.game.getScreenWidth()/2,100 + j*50))
                j += 1
                placeFlag = True

            if (j > number):
                break

            formatDataForOnePlayer = ' {0:3} {1:^10} {2:6d} {3:8.2f}'.format(j, *self.data[i])

            self.renderText(formatDataForOnePlayer,
                            self.fontLeaderBoard, (255, 255, 255),
                            (self.game.getScreenWidth()/2,100 + j*50))

            j += 1

            if (j > number):
                break

        if not placeFlag and j <= number:
            self.renderText('>{0:3} {1:^10} {2:6d} {3:8.2f}'.format(j, self.playerName[:10], self.game.getScore(), self.game.getTime()),
                            self.fontLeaderBoard, (255, 255, 255),
                            (self.game.getScreenWidth()/2,100 + j*50))


        self.renderText(' {0:^10} {1:>6} {2:>8}'.format('.....', '..', '.....'),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100 + (number + 1)*50))

        # for i in rows:

    def getScorePosition(self, score):
        counter = 1
        for i in self.sortedDataByScores:
            if i[1][1] < score:
                return counter
            else:
                counter += 1
        return counter


    def render(self):
        self.renderText('GAME OVER',
                        self.fontGameOver, (255, 255, 255),
                        (self.game.getScreenWidth()/2,50))

        self.renderText('Leaderboard',
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100))

        self.drawTableLB(5)

        self.renderText(' {0:3d} {1:^10} {2:6d} {3:8.2f}'.format(self.getScorePosition(self.game.getScore()), self.playerName[:10], self.game.getScore(), self.game.getTime()),
                        self.fontLeaderBoard, (255, 255, 255),
                        (self.game.getScreenWidth()/2,100 + 5*50 + 50 + 50))

        self.renderText('Back',
                        self.fontLeaderBoard if not self.isBackButton else self.fontLeaderBoardActive, (255, 255, 255),
                        (self.game.getScreenWidth()/2 - 100, self.game.getScreenHeight() - 80))

        self.renderText('Continue',
                        self.fontLeaderBoard if self.isBackButton else self.fontLeaderBoardActive, (255, 255, 255),
                        (self.game.getScreenWidth()/2 + 100, self.game.getScreenHeight() - 80))

    def control(self, event):
        if event.type == pygame.KEYDOWN and self.game.isGameOver:
            if event.key == pygame.K_RIGHT:
                self.isBackButton = False

            elif event.key == pygame.K_LEFT:
                self.isBackButton = True

            elif event.key == pygame.K_RETURN:
                self.saveResults()

                if self.isBackButton:
                    self.game.newGame()
                else:
                    self.game.newGame()

            elif event.key == pygame.K_BACKSPACE:
                self.playerName = self.playerName[:len(self.playerName) - 1]

            elif len(pygame.key.name(event.key)) == 1 and len(self.playerName) < 10:
                if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    self.playerName += pygame.key.name(event.key).upper()
                else:
                    self.playerName += pygame.key.name(event.key).lower()
                # self.playerName += self.game.charKeys[event.key]

    def saveResults(self):
        with open ('leaders.txt', 'r') as fileWithData:
            tmpData = fileWithData.readlines()
        fileWithData.close()

        newData = []
        for line in tmpData:
            if len(line.split()) == 3:
                if not (line.split()[0].rstrip() == self.playerName.rstrip()):
                    newData.append(line)

        newData.append('{0} {1} {2:.2f}\n'.format(self.playerName, self.game.getScore(), self.game.getTime()))

        with open ('leaders.txt', 'w') as fileWithData:
            fileWithData.writelines(newData)
        fileWithData.close()
