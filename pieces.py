"""Фигуры Тетриса: их формы, поворот и положение на поле.

Этот модуль ничего не знает про pygame — только данные и простые вычисления.
"""

import random

from board import WIDTH


# Формы всех 7 фигур. Каждая форма — это маленькая «картинка» из строк:
#   "X" — клетка занята блоком,
#   "." — клетка пустая.
# Все картинки квадратные (2×2, 3×3 или 4×4) — так их проще поворачивать.
# Например, T выглядит так:
#   . X .
#   X X X
#   . . .
SHAPES = {
    "I": ["....",
          "XXXX",
          "....",
          "...."],
    "O": ["XX",
          "XX"],
    "T": [".X.",
          "XXX",
          "..."],
    "S": [".XX",
          "XX.",
          "..."],
    "Z": ["XX.",
          ".XX",
          "..."],
    "J": ["X..",
          "XXX",
          "..."],
    "L": ["..X",
          "XXX",
          "..."],
}


def rotate_shape(shape):
    """Возвращает новую форму, повёрнутую на 90° по часовой стрелке.

    Исходная форма не меняется.
    """
    n = len(shape)  # размер квадрата: 2, 3 или 4
    new_shape = []
    for r in range(n):
        # Новая строка r собирается из столбца r старой формы,
        # но читается снизу вверх. Формула: new[r][c] = old[n-1-c][r].
        #
        # Пример на T:      .X.        .X.
        #                   XXX   ->   .XX
        #                   ...        .X.
        # Строка 1 новой формы = столбец 1 старой, прочитанный снизу вверх:
        # old[2][1], old[1][1], old[0][1] = ".", "X", "X" -> ".XX".
        new_row = ""
        for c in range(n):
            new_row += shape[n - 1 - c][r]
        new_shape.append(new_row)
    return new_shape


class Piece:
    """Фигура на поле: какая это фигура, её форма и где она находится.

    row и col — координаты левого верхнего угла «картинки» формы на поле
    (строка 0 — самая верхняя строка поля).
    """

    def __init__(self, letter, shape, row, col):
        self.letter = letter  # буква фигуры: "I", "O", "T", ...
        self.shape = shape    # форма (список строк, см. SHAPES)
        self.row = row        # строка поля, где верх формы
        self.col = col        # столбец поля, где левый край формы

    def cells(self):
        """Список клеток поля (row, col), которые занимает фигура."""
        result = []
        for r, line in enumerate(self.shape):
            for c, symbol in enumerate(line):
                if symbol == "X":
                    result.append((self.row + r, self.col + c))
        return result

    def moved(self, d_row, d_col):
        """Новая фигура, сдвинутая на d_row строк и d_col столбцов.

        Мы не меняем текущую фигуру, а создаём копию. Так игра может
        «примерить» ход и отказаться от него, если он недопустим.
        """
        return Piece(self.letter, self.shape, self.row + d_row, self.col + d_col)

    def rotated(self):
        """Новая фигура, повёрнутая на 90° по часовой стрелке (на том же месте)."""
        return Piece(self.letter, rotate_shape(self.shape), self.row, self.col)


def spawn_piece(letter):
    """Новая фигура с буквой letter в точке появления: строка 0, по центру поля."""
    shape = SHAPES[letter]
    width = len(shape[0])
    col = (WIDTH - width) // 2  # например, для O: (10 - 2) // 2 = 4
    return Piece(letter, shape, 0, col)


def random_piece():
    """Новая случайная фигура в точке появления."""
    letter = random.choice(list(SHAPES))
    return spawn_piece(letter)
