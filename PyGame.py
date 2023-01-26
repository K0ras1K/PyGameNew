import random
import os
# import sys
import time
import pygame


class Game:
    def __init__(self, xSize, ySize, bombSpawnChance, playerHp, bombDamage):
        self.mainBoard = MainBoard(xSize, ySize, bombSpawnChance)
        self.player = Player(playerHp)
        self.redBomb = RedBomb(bombDamage, self.mainBoard.getBombCoords())
        self.bombDamage = bombDamage
        self.activatedBomb = (-1, -1)
        self.gameOver = False
        self.bomb = False
        self.progress = 1

    def movePlayer(self, xCoord, yCoord):
        if self.canMove(xCoord, yCoord):
            self.mainBoard.mainBoardNetz[self.mainBoard.getPlayerCoords()[0]][self.mainBoard.getPlayerCoords()[1]], \
                self.mainBoard.mainBoardNetz[xCoord][yCoord] = 2, 3
            if self.redBomb.checkActivatedBomb(self.activatedBomb[0], self.activatedBomb[1], xCoord, yCoord):
                self.player.bombActivating(self.bombDamage)
            else:
                self.activatedBomb = (-1, -1)
            if self.redBomb.checkPlayer(xCoord, yCoord, self.mainBoard.getBombCoords()) != (-1, -1):
                self.activatedBomb = (self.redBomb.checkPlayer(xCoord, yCoord, self.mainBoard.getBombCoords()))
                # TODO Добавить вызывание звука активации бомбы
                mina.play()
            if self.player.HP == 0:
                self.gameOver = True
            self.progress += 1

    def canMove(self, xCoord, yCoord):
        if self.mainBoard.mainBoardNetz[xCoord][yCoord] == 2:
            return True
        return False

    # TODO Вызывать по нажатию пкм по квадратику
    def breakIce(self, xCoord, yCoord):
        if self.canBreakIce(xCoord, yCoord):
            self.mainBoard.breakIce(xCoord, yCoord)
        if self.redBomb.checkActivatedBomb(self.activatedBomb[0], self.activatedBomb[1],
                                           self.mainBoard.getPlayerCoords()[0], self.mainBoard.getPlayerCoords()[1]) and self.mainBoard.mainBoardNetz[self.activatedBomb[0]][self.activatedBomb[1]] == 1:
            self.player.bombActivating(self.bombDamage)
        else:
            self.activatedBomb = (-1, -1)
        if self.player.HP == 0:
            self.gameOver = True
            self.bomb = True
            boom.play()
        self.progress += 1

    def canBreakIce(self, xCoord, yCoord):
        if self.mainBoard.mainBoardNetz[xCoord][yCoord] != 2:
            if self.player.canBreakIce(xCoord, yCoord, self.mainBoard.getPlayerCoords()[0],
                                       self.mainBoard.getPlayerCoords()[1], self.progress):
                return True
        return False


class MainBoard:
    def __init__(self, xSize, ySize, bombSpawnChance):
        self.xSize = xSize
        self.ySize = ySize
        self.bombSpawnChance = bombSpawnChance
        self.mainBoardNetz = [[self.getBoolByChance(self.bombSpawnChance) for i in range(self.xSize)] for j in
                              range(self.ySize)]
        self.mainBoardNetz[0][0] = 3
        self.mainBoardNetz[1][0] = 0
        self.mainBoardNetz[1][1] = 0
        self.mainBoardNetz[0][1] = 0
        self.mainBoardNetz[9][9] = 0
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

    '''def printNetz(self):
        for i in self.mainBoardNetz:
            print(i)
        print()'''

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
        if abs(xCoord - lastX) <= 1 and abs(yCoord - lastY) <= 1:
            return True
        return False

    def setDeath(self):
        self.HP = 0


'''objects = []
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        self.alreadyPressed = False
        objects.append(self)
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)'''


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

ws = 0
gs = 0
pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50
cells = [
    load_image('ice50.png'),
    load_image('icebomb50.png'),
    load_image('land50.png'),
    load_image('player50.png'),
    load_image('finish50.png')
]
mina = pygame.mixer.Sound('./data/mina.mp3')
boom = pygame.mixer.Sound('./data/boom.mp3')
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
        elif pos_x == pos_y == 9:
            self.image = cells[-1]
        else:
            self.image = cells[self.cell_type]
        self.rect = self.image.get_rect().move(
            cell_width * pos_x, cell_height * pos_y)
        if cell_type == 3 and pos_x == pos_y == 9:
            game.gameOver = True

    def update(self, x, y, button):
        if self.rect.collidepoint(x, y):
            if button == 1:
                game.movePlayer(self.pos_x, self.pos_y)

            elif button == 3:
                game.breakIce(self.pos_x, self.pos_y)
                self.cell_type = 2
                if self.pos_x != 9 or self.pos_y != 9:
                    self.image = cells[self.cell_type]


clock = pygame.time.Clock()
sprite_group = SpriteGroup()
# hero_group = SpriteGroup()
game = Game(10, 10, 10, 3, 3)


'''def terminate():
    # выход
    pygame.quit()
    sys.exit'''


def start_screen():
    # стартовый экран
    intro_text = ["Правила игры:",
                  "Вы можете перемещать героя по клеткам земли,",
                  "вы можете сломать лёд рядом с героем,",
                  "сломанный лёд превращается в землю.",
                  "Подо льдом может находиться бомба, при",
                  "приближении к которой вы услышите",
                  "характерный звук из игры dota 2.",
                  "Чтобы избежать взрыва, надо либо отойти,",
                  "либо сломать клетку льда с бомбой.",
                  "Вы можете пережить лишь 1 взрыв.",
                  "Ваша цель - достичь финишной клетки.",
                  "Финишная клетка является льдинкой.",
                  "Перемещение героя - нажатие лкм по клетке.",
                  "Нажатие пкм разбивает лёд вместе с бомбой.",
                  "Нажмите любую кнопку, чтобы начать игру."]

    fon = pygame.transform.scale(load_image('white.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 28)
    text_coord = 16
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 25
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    # выход
    pygame.quit()


def end():
    pygame.quit()



def generate_level(level):
    # прорисовка уровня
    for y in range(len(level)):
        for x in range(len(level[y])):
            a = Cell(level[x][y], x, y)
            sprite_group.add(a)


def win_screen():
    text = ['Вы выиграли!',
            f'Вы выиграли {ws}/{gs} игр.',
            'Нажмите любую кнопку, чтобы продолжить',
            ' игру, или закройте это окно, чтобы',
            ' выйти из игры.'
            ]
    fon = pygame.transform.scale(load_image('white.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 25
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def loss_screen():
    text = ['Игра окончена!',
            f'Вы выиграли {ws}/{gs} игр.',
            'Нажмите любую кнопку, чтобы продолжить',
            ' игру, или закройте это окно, чтобы',
            ' выйти из игры.'
            ]
    fon = pygame.transform.scale(load_image('white.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 25
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
q = False
while True:
    w = False
    pygame.init()
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    sprite_group = SpriteGroup()
    game = Game(10, 10, 10, 3, 3)
    running = True
    q = False
    while running:
        generate_level(game.mainBoard.mainBoardNetz)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                q = True
            if game.gameOver == True:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    x, y = event.pos
                    sprite_group.update(x, y, event.button)
        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    if game.bomb:
        time.sleep(1.25)
    else:
        w = True
        ws += 1
    gs += 1
    if q:
        pygame.quit()
        break
    if w:
        win_screen()
    else:
        loss_screen()
