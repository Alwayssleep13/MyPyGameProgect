import pygame
import os

# Задаем начальные настройки
FPS = 60
clock = pygame.time.Clock()

pygame.init()
# Для атмосферы добавим музыку
pygame.mixer.music.load('напряженная.mp3')
# Теперь включаем ее
pygame.mixer.music.play()
# Называем игру
pygame.display.set_caption('Мини-лабринт')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
my_event = pygame.USEREVENT + 1
pygame.time.set_timer(my_event, 1000)

x = 810
y = 720
screen = pygame.display.set_mode((x, y))


# Функция обработки изображения
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# рисуем клетчатое поле
def field():
    for string in range(27):
        for row in range(24):
            y = row * 30
            x = string * 30
            pygame.draw.rect(screen, (0, 0, 0), (x + 0.5, y + 0.5, 29, 29))


# задаем игрока(нашу ходящюю точку в лабиринте)
class Player:
    def __init__(self):
        self.size = (31, 31)
        self.color = ((13, 140, 106), (5, 161, 161), (37, 115, 184))
        self.color_id = 0
        self.image = pygame.Surface((31, 31))
        self.image.fill(self.color[-1])
        self.rect = self.image.get_rect()
        self.rect.x = 359
        self.rect.y = 359
        self.cords = (self.rect.x, self.rect.y)

    def update(self):
        self.image.fill(self.color[self.color_id])
        self.color_id = (self.color_id + 1) % len(self.color)



# читка текстового документа с уровнем
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def init_coins() -> list:
    coins_coord = list()
    for index, value in enumerate(text_map):
        for index2, value2 in enumerate(value):
            if value2 == 'c':
                # проверка на наличие монеток
                coins_coord.append((index2 * 30 - 1, index * 30 - 1))
    return coins_coord


# функция, отвечающая за отрисовку монеток
def draw_coins(coins_coords):
    for x, y in coins_coords:
        pygame.draw.circle(screen, (255, 255, 0), (x + 16, y + 16), 10)


# функция, рисующая стены
def walls():
    for index, value in enumerate(text_map):
        for index2, value2 in enumerate(value):
            if value2 == 'w':
                # как с монеткой проверяем на наличие стены
                pygame.draw.rect(screen, (0, 0, 150), (index2*30-1, index*30-1, 31, 31))
                # отрисрвка стены
                global wall_cords
                # добавляем координаты стен с соотв. список
                wall_cords.append((index2*30-1, index*30-1))


# задаем окно заставки
def start_screen():
    intro_text = ["НАЙДИ СПОСОБ",
                  "ВЫБРАТЬСЯ ИЗ ЛАБИРИНТА",
                  f"score: {score}"]

    # теперь задаем фон
    fon = pygame.transform.scale(load_image('fon.jpg'), (x, y))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        # записываем текст на фон построчно
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# промежуточный экран
def finish_screen():
    intro_text = ["ТЕБЕ ИЗВЕСТЕН СПОСОБ, КАК",
                  "ВЫБРАТЬСЯ ИЗ ЛАБИРИНТА",
                  f"ТВОЙ СЧЕТ: {score}"]

    # теперь другой фон
    fon = pygame.transform.scale(load_image('пол.jpg'), (x, y))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        # аналогично с первым
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# НАКОНЕЦ ЗАКЛЮЧИТЕЛЬНЫЙ ЭКРАН
def end_screen():
    intro_text = ["ПОЗДРАВЛЯЮ!",
                  "ТЫ НАШЕЛ ВЫХОД!",
                  "ТЕПЕРЬ МОЖЕШЬ ИДТИ ДОМОЙ,",
                  "ТЫ ХОРОШО ПОРАБОТАЛ/ЛА.",
                  f"score: {score}"]

    # последняя стена
    fon = pygame.transform.scale(load_image('стена.jpg'), (x, y))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        # последняя запись
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  #закончили игру
        clock.tick(FPS)


# сначала отрисовка первого уровня
text_map = load_level('level1.txt')
# вызываем игрока
player = Player()
# список координат стен
wall_cords = []
# список координат монеток
coins_coord = init_coins()
# счет/кол-во монеток
score = 0
# запускаем стартовое окно
start_screen()

# объявляем флаги для возможности закончить игру
game_end = False
flag = False
# начинаем игру, уровень 1
while not game_end:
    if flag or score == 10:
        game_end = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = True
        if event.type == my_event:
            player.update()
        if event.type == pygame.KEYDOWN:
            # описываем реакцию перса на кнопки
            if event.key == pygame.K_LEFT:
                # при нажатии стрелки влево
                # проверка на стены
                if not (player.rect.x-30, player.rect.y) in wall_cords:
                    player.rect.x -= 30
                # проверка на монетки
                if (player.rect.x, player.rect.y) in coins_coord:
                    # если монетка, добаляем счет
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                # проверка на координаты, ведь это тоже один из способов закончить игруs
                if (player.rect.x, player.rect.y) == (719, 509):
                    flag = True
            # проводим такие же операции и проверки на другие кнопки
            if event.key == pygame.K_RIGHT:
                if not (player.rect.x+30, player.rect.y) in wall_cords:
                    player.rect.x += 30
                if (player.rect.x, player.rect.y) in coins_coord:
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                if (player.rect.x, player.rect.y) == (719, 509):
                    flag = True
            if event.key == pygame.K_UP:
                if not (player.rect.x, player.rect.y-30) in wall_cords:
                    player.rect.y -= 30
                if (player.rect.x, player.rect.y) in coins_coord:
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                if (player.rect.x, player.rect.y) == (719, 509):
                    flag = True
            if event.key == pygame.K_DOWN:
                if not (player.rect.x, player.rect.y+30) in wall_cords:
                    player.rect.y += 30
                if (player.rect.x, player.rect.y) in coins_coord:
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                if (player.rect.x, player.rect.y) == (659, 569):
                    flag = True
    # шаги после передвиж героя
    clock.tick(FPS)
    screen.fill((100, 100, 100))
    field()
    pygame.draw.rect(screen, player.color[player.color_id], (player.rect.x, player.rect.y, *player.size))
    walls()
    draw_coins(coins_coord)
    pygame.display.flip()

# показываем промежуточный экран
finish_screen()

# отрисовка и запуск 2 уровеня
text_map = load_level('level2.txt')

# обнуляем списки для нормальной работы второго уровня
wall_cords = []
coins_coord = init_coins()

# так же как для первого, прописываем условия для 2 уровня
game_end = False
flag = False
while not game_end:
    if flag or score == 25:
        game_end = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = True
        if event.type == my_event:
            player.update()
        if event.type == pygame.KEYDOWN:
            # повтор действий из первого уровня
            if event.key == pygame.K_LEFT:
                if not (player.rect.x-30, player.rect.y) in wall_cords:
                    player.rect.x -= 30
                if (player.rect.x, player.rect.y) in coins_coord:
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                if (player.rect.x, player.rect.y) == (719, 509):
                    flag = True
            if event.key == pygame.K_RIGHT:
                if not (player.rect.x+30, player.rect.y) in wall_cords:
                    player.rect.x += 30
                if (player.rect.x, player.rect.y) in coins_coord:
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                if (player.rect.x, player.rect.y) == (719, 509):
                    flag = True
            if event.key == pygame.K_UP:
                if not (player.rect.x, player.rect.y-30) in wall_cords:
                    player.rect.y -= 30
                if (player.rect.x, player.rect.y) in coins_coord:
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                if (player.rect.x, player.rect.y) == (719, 509):
                    flag = True
            if event.key == pygame.K_DOWN:
                if not (player.rect.x, player.rect.y+30) in wall_cords:
                    player.rect.y += 30
                if (player.rect.x, player.rect.y) in coins_coord:
                    score += 1
                    coins_coord.remove((player.rect.x, player.rect.y))
                if (player.rect.x, player.rect.y) == (659, 569):
                    flag = True

    clock.tick(FPS)
    screen.fill((100, 100, 100))
    field()
    pygame.draw.rect(screen, player.color[player.color_id], (player.rect.x, player.rect.y, *player.size))
    walls()
    draw_coins(coins_coord)
    pygame.display.flip()

# после завершения 2 уровня выводим заключиельный экран со счетом и закрываем игру
end_screen()
