import random


class Game:
    def __init__(self, xSize, ySize, bombSpawnChance, playerHp, bombDamage):
        self.mainBoard = MainBoard(xSize, ySize, bombSpawnChance)
        self.player = Player(playerHp)
        self.redBomb = RedBomb(bombDamage, self.mainBoard.getBombCoords())
        self.bombDamage = bombDamage
        self.activatedBomb = (-1, -1)
        #TODO При gameOver = True вызвать окно окончания игры
        self.gameOver = False

    #TODO Вызывать по нажатию лкм по квадратику поля
    def movePlayer(self, xCoord, yCoord):
        if self.canMove(xCoord, yCoord):
            self.mainBoard.mainBoardNetz[self.player.xCoord][self.player.yCoord] = 2
            self.player.move(xCoord, yCoord)
            self.mainBoard.mainBoardNetz[xCoord][yCoord] = 3
            self.mainBoard.printNetz()
            print()
            if self.redBomb.checkPlayer(xCoord, yCoord, self.mainBoard.getBombCoords()) != (-1, -1):
                self.activatedBomb = (self.redBomb.checkPlayer(xCoord, yCoord, self.mainBoard.getBombCoords()))
                #TODO Добавить вызывание звука активации бомбы
                print('Звук бомбы!')
                print()
            if self.redBomb.checkActivatedBomb(self.activatedBomb[0], self.activatedBomb[1], xCoord, yCoord):
                self.player.bombActivating(self.bombDamage)
            else:
                self.activatedBomb = (-1, -1)
            if self.player.HP == 0:
                self.gameOver = True
                print('Игра окончена')
                print()
        else:
            print('Нельзя!')
            print()

    def canMove(self, xCoord, yCoord):
        if self.mainBoard.mainBoardNetz[xCoord][yCoord] == 2:
            return True
        return False


    #TODO Вызывать по нажатию пкм по квадратику
    def breakIce(self, xCoord, yCoord):
        if self.player.canBreakIce(xCoord, yCoord):
            if self.canBreakIce(xCoord, yCoord):
                self.mainBoard.breakIce(xCoord, yCoord)
        if self.redBomb.checkActivatedBomb(self.activatedBomb[0], self.activatedBomb[1], self.player.xCoord, self.player.yCoord):
            self.player.bombActivating(self.bombDamage)
        else:
            self.activatedBomb = (-1, -1)
        if self.player.HP == 0:
            self.gameOver = True
        self.mainBoard.printNetz()

    def canBreakIce(self, xCoord, yCoord):
        if self.mainBoard.mainBoardNetz[xCoord][yCoord] != 2:
            if self.player.canBreakIce(xCoord, yCoord):
                return True


class MainBoard:
    def __init__(self, xSize, ySize, bombSpawnChance):
        self.xSize = xSize
        self.ySize = ySize
        self.bombSpawnChance = bombSpawnChance
        self.mainBoardNetz = [[self.getBoolByChance(self.bombSpawnChance) for i in range(self.xSize)] for j in
                              range(self.ySize)]
        self.mainBoardNetz[0][0] = 3
        for i in self.mainBoardNetz:
            print(i)
        print()

    def getBoolByChance(self, chance):
        if random.random() < chance / 100:
            return 1
        return 0

    def breakIce(self, xCoord, yCoord):
        self.mainBoardNetz[xCoord][yCoord] = 2

    def getBombCoords(self):
        bombCoords = []
        for i in range(len(self.mainBoardNetz)):
            for j in range(len(self.mainBoardNetz[0])):
                if self.mainBoardNetz[i][j] == 1:
                    bombCoords.append((i, j))
        return bombCoords

    def printNetz(self):
        for i in self.mainBoardNetz:
            print(i)
        print()


class RedBomb:
    def __init__(self, bombDamage, bombCoords):
        self.bombDamage = bombDamage
        self.bombCoords = bombCoords

    def checkPlayer(self, xCoord, yCoord, bombCoords):
        for i in bombCoords:
            if abs(i[0] - xCoord) <= 1 and abs(i[1] - yCoord) <= 1:
                return (i[0], i[1])
        return (-1, -1)

    def checkActivatedBomb(self, xCoordBomb, yCoordBomb, xCoord, yCoord):
        if (xCoordBomb == -1 or yCoordBomb == -1):
            return False
        if abs(xCoordBomb - xCoord) <= 1 and abs(yCoordBomb - yCoord) <= 1:
            return True
        return False




class Player:
    def __init__(self, HP):
        self.xCoord = 0
        self.yCoord = 0
        self.HP = HP
        self.progress = 1

    def bombActivating(self, damage):
        if self.HP - damage > 0:
            self.HP -= damage
        else:
            self.setDeadth()

    def move(self, xCoord, yCoord):
        if self.progress % 2 != 0:
            return
        if abs(xCoord - self.xCoord) <= 1 and abs(yCoord - self.yCoord) <= 1:
            self.xCoord = xCoord
            self.yCoord = yCoord
        self.progress += 1

    def canBreakIce(self, xCoord, yCoord):
        if self.progress % 2 != 1:
            return False
        if abs(xCoord - self.xCoord) <= 1 and abs(yCoord - self.yCoord) <= 1:
            return True
        return False

    def setDeadth(self):
        self.HP = 0


