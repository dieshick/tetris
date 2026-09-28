"""Тесты для фигур: формы, поворот, положение на поле."""

from pieces import SHAPES, Piece, rotate_shape


def test_rotate_t_clockwise():
    # T «носом вверх» после поворота смотрит вправо
    assert rotate_shape(SHAPES["T"]) == [".X.", ".XX", ".X."]


def test_rotate_i_to_vertical():
    assert rotate_shape(SHAPES["I"]) == ["..X.", "..X.", "..X.", "..X."]


def test_four_rotations_return_original():
    # Четыре поворота по 90° — это полный круг
    for letter, shape in SHAPES.items():
        s = shape
        for _ in range(4):
            s = rotate_shape(s)
        assert s == shape, letter


def test_cells_use_position():
    piece = Piece("T", SHAPES["T"], 0, 3)
    assert sorted(piece.cells()) == [(0, 4), (1, 3), (1, 4), (1, 5)]


def test_moved_and_rotated_do_not_change_original():
    piece = Piece("T", SHAPES["T"], 0, 3)
    moved = piece.moved(2, -1)
    rotated = piece.rotated()
    assert (moved.row, moved.col) == (2, 2)
    assert rotated.shape == [".X.", ".XX", ".X."]
    # Исходная фигура осталась прежней
    assert (piece.row, piece.col, piece.shape) == (0, 3, SHAPES["T"])
