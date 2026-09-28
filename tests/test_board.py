"""Тесты для игрового поля: границы, столкновения, фиксация, очистка линий."""

from board import HEIGHT, WIDTH, Board
from pieces import SHAPES, Piece


def o_at(row, col):
    """Фигура O (квадрат 2×2) в заданной позиции."""
    return Piece("O", SHAPES["O"], row, col)


def full_row():
    """Полностью заполненная строка поля."""
    return ["X"] * WIDTH


def test_new_board_is_empty():
    board = Board()
    assert len(board.grid) == HEIGHT
    assert all(cell is None for row in board.grid for cell in row)


def test_walls_and_floor():
    board = Board()
    assert board.is_valid_position(o_at(0, 0))
    assert board.is_valid_position(o_at(0, 8))
    assert not board.is_valid_position(o_at(0, -1))   # за левой стенкой
    assert not board.is_valid_position(o_at(0, 9))    # за правой стенкой
    assert board.is_valid_position(o_at(18, 0))
    assert not board.is_valid_position(o_at(19, 0))   # ниже дна


def test_cells_above_board_are_valid():
    assert Board().is_valid_position(o_at(-1, 4))


def test_overlap_with_occupied_cell():
    board = Board()
    board.grid[5][5] = "Z"
    assert not board.is_valid_position(o_at(4, 4))


def test_lock_piece_writes_letter():
    board = Board()
    board.lock_piece(o_at(18, 0))
    assert board.grid[18][0] == "O" and board.grid[19][1] == "O"


def test_clear_one_line_shifts_rows_down():
    board = Board()
    board.grid[19] = full_row()
    board.grid[18][0] = "T"
    assert board.clear_full_lines() == 1
    assert board.grid[19][0] == "T"
    assert all(cell is None for cell in board.grid[0])
    assert len(board.grid) == HEIGHT


def test_clear_four_lines():
    board = Board()
    for r in range(16, 20):
        board.grid[r] = full_row()
    assert board.clear_full_lines() == 4
    assert all(cell is None for row in board.grid for cell in row)


def test_clear_non_adjacent_lines():
    board = Board()
    board.grid[19] = full_row()
    board.grid[17] = full_row()
    board.grid[18][2] = "S"
    board.grid[16][7] = "Z"
    assert board.clear_full_lines() == 2
    assert board.grid[19][2] == "S"
    assert board.grid[18][7] == "Z"
    assert sum(cell is not None for row in board.grid for cell in row) == 2
