import random
import os
# import sys
import pygame


class Game:
    def __init__(self, xSize, ySize, bombSpawnChance, playerHp, bombDamage):
        self.mainBoard = MainBoard(xSize, ySize, bombSpawnChance)
        self.player = Player(playerHp)
        self.redBomb = RedBomb(bombDamage, self.mainBoard.getBombCoords())
        self.bombDamage = bombDamage
        self.activatedBomb = (-1, -1)
        # TODO При gameOver = True вызвать окно окончания игры
        self.gameOver = False
        self.progress = 1

    # TODO Вызывать по нажатию лкм по квадратику поля
    def movePlayer(self, xCoord, yCoord):
        if self.canMove(xCoord, yCoord):
            self.mainBoard.mainBoardNetz[self.mainBoard.getPlayerCoords()[0]][self.mainBoard.getPlayerCoords()[1]], \
                self.mainBoard.mainBoardNetz[xCoord][yCoord] = 2, 3
            self.mainBoard.printNetz()
            print()
            if self.redBomb.checkActivatedBomb(self.activatedBomb[0], self.activatedBomb[1], xCoord, yCoord):
                self.player.bombActivating(self.bombDamage)
            else:
                self.activatedBomb = (-1, -1)
            if self.redBomb.checkPlayer(xCoord, yCoord, self.mainBoard.getBombCoords()) != (-1, -1):
                self.activatedBomb = (self.redBomb.checkPlayer(xCoord, yCoord, self.mainBoard.getBombCoords()))
                # TODO Добавить вызывание звука активации бомбы
                print('Звук бомбы!')
                print(self.activatedBomb)
                print()
            if self.player.HP == 0:
                self.gameOver = True
                print('Игра окончена')
                print()
            self.progress += 1
        else:
            print('Нельзя! move')
            print()

    def canMove(self, xCoord, yCoord):
        if self.mainBoard.mainBoardNetz[xCoord][yCoord] == 2:
            return True
        return False

    # TODO Вызывать по нажатию пкм по квадратику
    def breakIce(self, xCoord, yCoord):
        if self.canBreakIce(xCoord, yCoord):
            self.mainBoard.breakIce(xCoord, yCoord)
        if self.redBomb.checkActivatedBomb(self.activatedBomb[0], self.activatedBomb[1],
                                           self.mainBoard.getPlayerCoords()[0], self.mainBoard.getPlayerCoords()[1]):
            self.player.bombActivating(self.bombDamage)
        else:
            self.activatedBomb = (-1, -1)
        if self.player.HP == 0:
            self.gameOver = True
            print("Game Over")
        self.progress += 1
        self.mainBoard.printNetz()

    def canBreakIce(self, xCoord, yCoord):
        if self.mainBoard.mainBoardNetz[xCoord][yCoord] != 2:
            if self.player.canBreakIce(xCoord, yCoord, self.mainBoard.getPlayerCoords()[0],
                                       self.mainBoard.getPlayerCoords()[1], self.progress):
                return True
        print("Нельзя break")
        return False


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

    def getPlayerCoords(self):
        for i in range(len(self.mainBoardNetz)):
            for j in range(len(self.mainBoardNetz[0])):
                if self.mainBoardNetz[i][j] == 3:
                    return (i, j)


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
        self.HP = HP
        self.progress = 1

    def bombActivating(self, damage):
        if self.HP - damage > 0:
            self.HP -= damage
        else:
            self.setDeath()

    def canMove(self, xCoord, yCoord, lastX, lastY, progress):
        if progress % 2 != 0:
            return False
        if abs(xCoord - lastX) <= 1 and abs(yCoord - lastY) <= 1:
            return True
        return False

    def canBreakIce(self, xCoord, yCoord, lastX, lastY, progress):
        # if progress % 2 != 1:
        #     return False
        if abs(xCoord - lastX) <= 1 and abs(yCoord - lastY) <= 1:
            return True
        return False

    def setDeath(self):
        self.HP = 0


def load_image(name, color_key=None):
    # загрузка картинок в игру
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    # очистка фона, если нужно
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50
cells = [
    load_image('ice50.png'),
    load_image('icebomb50.png'),
    load_image('land50.png'),
    load_image('player50.png')
]
cell_width = cell_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    # экранный объект
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 1000, 1000)


class SpriteGroup(pygame.sprite.Group):
    # определение групп подвижных/неподвижных спрайтов
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)

    def update(self, x, y, button):
        for sprite in self:
            sprite.update(x, y, button)


class Sprite(pygame.sprite.Sprite):
    # определение групп подвижных/неподвижных спрайтов
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Cell(Sprite):
    # клетки
    def __init__(self, cell_type, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.detected = False
        self.cell_type = cell_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        if cell_type == 1 and not self.detected:
            self.image = cells[0]
        else:
            self.image = cells[self.cell_type]
        self.rect = self.image.get_rect().move(
            cell_width * pos_x, cell_height * pos_y)

    def update(self, x, y, button):
        if self.rect.collidepoint(x, y):
            print(self.pos_x, self.pos_y)
            if button == 1:
                game.movePlayer(self.pos_x, self.pos_y)

            elif button == 3:
                game.breakIce(self.pos_x, self.pos_y)
                self.cell_type = 2
                self.image = cells[self.cell_type]


clock = pygame.time.Clock()
sprite_group = SpriteGroup()
# hero_group = SpriteGroup()
game = Game(10, 10, 10, 3, 3)


'''def terminate():
    # выход
    pygame.quit()
    sys.exit'''


'''def start_screen():
    # стартовый экран

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)'''


def generate_level(level):
    # прорисовка уровня
    for y in range(len(level)):
        for x in range(len(level[y])):
            a = Cell(level[y][x], x, y)
            sprite_group.add(a)


# def move(hero, movement):
# движение героя

running = True
while running:
    generate_level(game.mainBoard.mainBoardNetz)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                x, y = event.pos
                print(x, y)
                sprite_group.update(x, y, event.button)
    screen.fill(pygame.Color("black"))
    sprite_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
