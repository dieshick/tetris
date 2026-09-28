"""Игровое поле Тетриса: какие клетки заняты, столкновения, очистка линий.

Этот модуль ничего не знает про pygame. Про фигуру ему достаточно знать
одно: у неё есть метод cells(), который возвращает занятые клетки.
"""

WIDTH = 10   # столбцов на поле
HEIGHT = 20  # строк на поле


class Board:
    """Поле 10×20.

    grid — список из HEIGHT строк, в каждой WIDTH клеток.
    Строка 0 — самая верхняя. Клетка хранит:
      None — если пустая,
      букву фигуры ("T", "I", ...) — если занята (по букве выбирается цвет).
    """

    def __init__(self):
        self.grid = [self._empty_row() for _ in range(HEIGHT)]

    def _empty_row(self):
        """Новая пустая строка поля."""
        return [None] * WIDTH

    def is_valid_position(self, piece):
        """True, если фигура может стоять в своей текущей позиции.

        Позиция допустима, если каждая клетка фигуры:
          - не выходит за левую/правую стенку и за дно;
          - не попадает на уже занятую клетку.
        Клетки выше поля (row < 0) разрешены — фигура может «торчать» сверху.
        """
        for row, col in piece.cells():
            if col < 0 or col >= WIDTH:
                return False  # за стенкой
            if row >= HEIGHT:
                return False  # ниже дна
            if row >= 0 and self.grid[row][col] is not None:
                return False  # клетка уже занята
        return True

    def lock_piece(self, piece):
        """«Впечатывает» фигуру в поле: её клетки становятся занятыми."""
        for row, col in piece.cells():
            self.grid[row][col] = piece.letter

    def clear_full_lines(self):
        """Удаляет заполненные строки и возвращает, сколько их было.

        Идея: оставляем только НЕзаполненные строки (в них есть хотя бы
        одна пустая клетка), а сверху добавляем столько пустых строк,
        сколько удалили. Поскольку оставшиеся строки идут в прежнем порядке,
        всё, что было над удалёнными строками, само «опускается» вниз.
        """
        remaining = [row for row in self.grid if None in row]
        cleared = HEIGHT - len(remaining)
        new_rows = [self._empty_row() for _ in range(cleared)]
        self.grid = new_rows + remaining
        return cleared
