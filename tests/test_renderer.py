"""Проверка, что отрисовка не падает. Картинку проверяем глазами, запустив игру."""

import os

# Рисуем без настоящего окна — так тест работает где угодно
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from game import Game
from renderer import WINDOW_SIZE, draw


def test_draw_does_not_crash():
    pygame.init()
    screen = pygame.Surface(WINDOW_SIZE)
    game = Game()
    game.board.grid[19][0] = "L"
    draw(screen, game)
    game.game_over = True   # экран «Игра окончена» тоже должен рисоваться
    draw(screen, game)
    pygame.quit()
