"""Отрисовка игры на экране с помощью pygame.

Здесь только рисование: функция draw() читает состояние Game и ничего в нём
не меняет. Вся логика игры живёт в game.py.
"""

import pygame

from board import HEIGHT, WIDTH

CELL = 30                                  # размер клетки в пикселях
PANEL_WIDTH = 200                          # ширина панели справа
FIELD_WIDTH = WIDTH * CELL                 # 300 px
FIELD_HEIGHT = HEIGHT * CELL               # 600 px
WINDOW_SIZE = (FIELD_WIDTH + PANEL_WIDTH, FIELD_HEIGHT)  # (500, 600)

# Цвета в формате (красный, зелёный, синий), каждый от 0 до 255
BACKGROUND = (20, 20, 30)
GRID_LINE = (40, 40, 55)
PANEL_BACKGROUND = (30, 30, 45)
TEXT_COLOR = (230, 230, 230)

# Классические цвета фигур
COLORS = {
    "I": (0, 240, 240),    # голубой
    "O": (240, 240, 0),    # жёлтый
    "T": (160, 0, 240),    # фиолетовый
    "S": (0, 240, 0),      # зелёный
    "Z": (240, 0, 0),      # красный
    "J": (0, 0, 240),      # синий
    "L": (240, 160, 0),    # оранжевый
}
# Цвет для клеток с неизвестной буквой (на всякий случай)
UNKNOWN_COLOR = (128, 128, 128)

# Шрифты создаются один раз и запоминаются здесь: создавать их
# заново на каждом кадре (60 раз в секунду) было бы медленно.
_fonts = {}


def _font(size):
    """Шрифт нужного размера. Arial умеет рисовать русские буквы."""
    if size not in _fonts:
        _fonts[size] = pygame.font.SysFont("arial", size)
    return _fonts[size]


def draw(screen, game):
    """Нарисовать весь кадр: поле, фигуру, панель и (если нужно) «Игра окончена»."""
    screen.fill(BACKGROUND)
    _draw_grid_lines(screen)
    _draw_board(screen, game.board)
    if not game.game_over:
        _draw_piece(screen, game.current)
    _draw_panel(screen, game)
    if game.game_over:
        _draw_game_over(screen)


def _draw_cell(screen, row, col, letter):
    """Нарисовать одну клетку поля цветом фигуры."""
    if row < 0:
        return  # клетка выше поля — её не видно
    color = COLORS.get(letter, UNKNOWN_COLOR)
    rect = pygame.Rect(col * CELL, row * CELL, CELL, CELL)
    # Рисуем чуть меньше клетки, чтобы между блоками были видны щели
    pygame.draw.rect(screen, color, rect.inflate(-2, -2))


def _draw_grid_lines(screen):
    """Тонкая сетка на поле."""
    for col in range(WIDTH + 1):
        x = col * CELL
        pygame.draw.line(screen, GRID_LINE, (x, 0), (x, FIELD_HEIGHT))
    for row in range(HEIGHT + 1):
        y = row * CELL
        pygame.draw.line(screen, GRID_LINE, (0, y), (FIELD_WIDTH, y))


def _draw_board(screen, board):
    """Все уже упавшие (занятые) клетки поля."""
    for row in range(HEIGHT):
        for col in range(WIDTH):
            letter = board.grid[row][col]
            if letter is not None:
                _draw_cell(screen, row, col, letter)


def _draw_piece(screen, piece):
    """Фигура, которая сейчас падает."""
    for row, col in piece.cells():
        _draw_cell(screen, row, col, piece.letter)


def _draw_panel(screen, game):
    """Панель справа: счёт, уровень, линии."""
    panel = pygame.Rect(FIELD_WIDTH, 0, PANEL_WIDTH, FIELD_HEIGHT)
    pygame.draw.rect(screen, PANEL_BACKGROUND, panel)

    x = FIELD_WIDTH + 20
    y = 30
    for title, value in (("Счёт", game.score), ("Уровень", game.level), ("Линии", game.lines)):
        _draw_text(screen, title, 24, (x, y))
        _draw_text(screen, str(value), 36, (x, y + 28))
        y += 90


def _draw_game_over(screen):
    """Затемнить поле и написать «Игра окончена»."""
    # Отдельная поверхность с прозрачностью (альфа 180 из 255)
    shade = pygame.Surface((FIELD_WIDTH, FIELD_HEIGHT), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 180))
    screen.blit(shade, (0, 0))

    center_x = FIELD_WIDTH // 2
    center_y = FIELD_HEIGHT // 2
    _draw_text(screen, "Игра окончена", 36, (center_x, center_y - 20), centered=True)
    _draw_text(screen, "R — заново", 24, (center_x, center_y + 20), centered=True)


def _draw_text(screen, text, size, position, centered=False):
    """Написать текст. position — левый верхний угол или центр (если centered)."""
    image = _font(size).render(text, True, TEXT_COLOR)
    rect = image.get_rect()
    if centered:
        rect.center = position
    else:
        rect.topleft = position
    screen.blit(image, rect)
