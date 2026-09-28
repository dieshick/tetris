"""Тесты обработки клавиш в главном цикле."""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from game import Game
from main import handle_event
from pieces import spawn_piece


def key_down(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def key_up(key):
    return pygame.event.Event(pygame.KEYUP, key=key)


def test_holding_space_drops_only_one_piece():
    game = Game(next_piece=lambda: spawn_piece("O"))
    held = set()
    handle_event(game, key_down(pygame.K_SPACE), held)
    # Автоповтор присылает KEYDOWN снова, пока клавиша зажата
    handle_event(game, key_down(pygame.K_SPACE), held)
    handle_event(game, key_down(pygame.K_SPACE), held)
    assert game.board.grid[19][4] == "O"
    assert game.board.grid[17][4] is None   # упала только одна фигура

    # Отпустили и нажали снова — вторая фигура падает
    handle_event(game, key_up(pygame.K_SPACE), held)
    handle_event(game, key_down(pygame.K_SPACE), held)
    assert game.board.grid[17][4] == "O"


def test_holding_left_repeats_move():
    game = Game(next_piece=lambda: spawn_piece("O"))
    held = set()
    for _ in range(3):
        handle_event(game, key_down(pygame.K_LEFT), held)
    assert game.current.col == 1


def test_quit_and_escape_stop_the_game():
    game = Game()
    assert handle_event(game, pygame.event.Event(pygame.QUIT), set()) is False
    assert handle_event(game, key_down(pygame.K_ESCAPE), set()) is False
    assert handle_event(game, key_down(pygame.K_LEFT), set()) is True
