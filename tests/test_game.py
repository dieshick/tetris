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


# --- Очки и уровни ---

def fill_bottom_row_except_4_5(game):
    """Заполнить нижнюю строку, оставив дырку ровно под фигуру O."""
    for c in range(10):
        if c not in (4, 5):
            game.board.grid[19][c] = "X"


def test_line_clear_scores_times_level():
    game = make_game()
    game.level, game.lines = 3, 20
    fill_bottom_row_except_4_5(game)
    game.hard_drop()                   # 36 за сброс + 100 × 3 за линию
    assert game.score == 336
    assert game.lines == 21


def test_level_up_after_ten_lines():
    game = make_game()
    game.lines = 9
    fill_bottom_row_except_4_5(game)
    game.hard_drop()
    assert game.lines == 10
    assert game.level == 2
    assert game.score == 36 + 100      # очки считаются по старому уровню


def test_fall_interval():
    game = make_game()
    assert game.fall_interval() == 800
    game.level = 2
    assert game.fall_interval() == 730
    game.level = 11
    assert game.fall_interval() == 100
    game.level = 15
    assert game.fall_interval() == 100


# --- Падение со временем ---

def test_update_falls_only_after_interval():
    game = make_game()
    game.update(799)
    assert game.current.row == 0
    game.update(1)
    assert game.current.row == 1
    assert game.score == 0


def test_huge_dt_drops_only_current_piece():
    # Если прошло очень много времени (например, окно перетаскивали),
    # фигура падает до дна и фиксируется, а остаток времени сбрасывается —
    # игра не проигрывается сама собой.
    game = make_game()
    game.update(1_000_000)
    assert game.board.grid[19][4] == "O"
    assert game.board.grid[17][4] is None   # легла только одна фигура
    assert not game.game_over
    assert game.current.row == 0


# --- Конец игры и рестарт ---

def test_game_over_when_spawn_is_blocked():
    game = make_game()
    game.current = game.current.moved(0, -4)
    game.board.grid[1][5] = "Z"
    game.hard_drop()
    assert game.game_over


def test_commands_ignored_after_game_over():
    game = make_game()
    game.game_over = True
    before = (game.score, game.current.row, game.current.col)
    game.move_left()
    game.move_right()
    game.rotate()
    game.soft_drop()
    game.hard_drop()
    game.update(10_000)
    assert (game.score, game.current.row, game.current.col) == before


def test_restart_resets_state():
    game = make_game()
    game.hard_drop()
    game.level, game.lines, game.game_over = 4, 33, True
    game.restart()
    assert (game.score, game.level, game.lines, game.game_over) == (0, 1, 0, False)
    assert all(cell is None for row in game.board.grid for cell in row)
    assert game.current.row == 0
