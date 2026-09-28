"""Правила Тетриса: движение фигуры, сбросы, очки, уровни, конец игры.

Класс Game хранит всё состояние игры. Он ничего не знает про pygame:
main.py вызывает его методы при нажатии клавиш, а renderer.py читает
его атрибуты, чтобы нарисовать картинку.
"""

from board import Board
from pieces import random_piece


# Очки за одновременно очищенные линии (потом умножаются на уровень).
LINE_SCORES = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}


class Game:
    """Состояние и правила одной игры."""

    def __init__(self, next_piece=random_piece):
        # next_piece — функция, которая выдаёт новую фигуру.
        # В игре это random_piece (случайные фигуры), а в тестах можно
        # передать свою функцию, чтобы фигуры были заранее известны.
        self.next_piece = next_piece
        self.board = Board()
        self.current = self.next_piece()  # фигура, которой управляет игрок
        self.score = 0
        self.level = 1
        self.lines = 0          # сколько линий очищено за игру
        self.game_over = False
        self.fall_timer = 0     # сколько мс накопилось до следующего шага падения

    # --- Команды игрока ---

    def move_left(self):
        """Сдвинуть фигуру на клетку влево (если есть место)."""
        self._try_move(0, -1)

    def move_right(self):
        """Сдвинуть фигуру на клетку вправо (если есть место)."""
        self._try_move(0, 1)

    def rotate(self):
        """Повернуть фигуру по часовой стрелке.

        Если повёрнутая фигура не помещается, пробуем сдвинуть её
        на 1 клетку влево, потом на 1 вправо («отталкивание» от стенки).
        Если ничего не подошло — поворот отменяется.
        """
        rotated = self.current.rotated()
        for d_col in (0, -1, 1):
            candidate = rotated.moved(0, d_col)
            if self.board.is_valid_position(candidate):
                self.current = candidate
                return

    def soft_drop(self):
        """Опустить фигуру на 1 клетку (+1 очко). Если ниже некуда — зафиксировать."""
        if self._try_move(1, 0):
            self.score += 1
        else:
            self._lock_current()

    def hard_drop(self):
        """Уронить фигуру до упора (+2 очка за каждую клетку) и зафиксировать."""
        distance = 0
        while self._try_move(1, 0):
            distance += 1
        self.score += 2 * distance
        self._lock_current()

    # --- Внутренние помощники ---

    def _try_move(self, d_row, d_col):
        """Сдвинуть фигуру, если новая позиция допустима. Возвращает True при успехе."""
        candidate = self.current.moved(d_row, d_col)
        if self.board.is_valid_position(candidate):
            self.current = candidate
            return True
        return False

    def _lock_current(self):
        """Фигура легла: впечатать её, очистить линии, начислить очки, выдать новую."""
        self.board.lock_piece(self.current)

        cleared = self.board.clear_full_lines()
        # Очки считаем по уровню ДО того, как он мог вырасти
        self.score += LINE_SCORES[cleared] * self.level
        self.lines += cleared
        self.level = 1 + self.lines // 10  # каждые 10 линий — новый уровень

        self.current = self.next_piece()
        self.fall_timer = 0
        # Если новой фигуре негде появиться — игра окончена
        if not self.board.is_valid_position(self.current):
            self.game_over = True
