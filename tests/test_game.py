"""Тесты для правил игры."""

from game import Game
from pieces import spawn_piece


def make_game(letter="O"):
    """Игра, в которой всегда появляется одна и та же фигура — для предсказуемых тестов."""
    return Game(next_piece=lambda: spawn_piece(letter))


# --- Движение и поворот ---

def test_move_stops_at_left_wall():
    game = make_game("T")
    for _ in range(10):
        game.move_left()
    assert game.current.col == 0


def test_move_stops_at_right_wall():
    game = make_game("T")
    for _ in range(10):
        game.move_right()
    assert game.current.col == 7


def test_rotate_kicks_away_from_wall():
    game = make_game("T")
    game.rotate()                      # T смотрит вправо: [".X.", ".XX", ".X."]
    for _ in range(10):
        game.move_left()
    assert game.current.col == -1
    game.rotate()                      # на месте не влезает, влево тоже, вправо — да
    assert game.current.shape == ["...", "XXX", ".X."]
    assert game.current.col == 0


def test_rotate_cancelled_when_no_kick_fits():
    game = make_game("I")
    game.rotate()                      # вертикальная I, блоки в столбце формы 2
    for _ in range(10):
        game.move_left()
    assert game.current.col == -2
    game.rotate()
    assert game.current.shape == ["..X."] * 4
    assert game.current.col == -2


# --- Сбросы ---

def test_soft_drop_moves_down_and_scores():
    game = make_game()
    game.soft_drop()
    assert game.current.row == 1 and game.score == 1


def test_hard_drop_scores_and_locks():
    game = make_game()
    game.hard_drop()                   # O падает с 0 на 18 строку
    assert game.score == 36
    assert game.board.grid[18][4] == "O" and game.board.grid[19][5] == "O"
    assert game.current.row == 0       # появилась новая фигура


def test_hard_drop_with_no_room_to_fall():
    game = make_game()
    game.board.grid[2][4] = "Z"
    game.hard_drop()
    assert game.score == 0
    assert game.board.grid[0][4] == "O"


def test_soft_drop_on_floor_locks():
    game = make_game()
    game.current = game.current.moved(18, 0)
    game.soft_drop()
    assert game.board.grid[19][4] == "O"
    assert game.score == 0
