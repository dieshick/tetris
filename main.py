"""Запуск игры: окно, главный цикл, обработка клавиш.

Запуск:  python main.py
"""

import pygame

from game import Game
from renderer import WINDOW_SIZE, draw

FPS = 60  # кадров в секунду


def handle_key(game, key):
    """Перевести нажатую клавишу в команду игры.

    Возвращает False, если игрок хочет выйти (Esc), иначе True.
    """
    if key == pygame.K_ESCAPE:
        return False
    if game.game_over:
        # После конца игры работает только R — начать заново
        if key == pygame.K_r:
            game.restart()
        return True

    if key == pygame.K_LEFT:
        game.move_left()
    elif key == pygame.K_RIGHT:
        game.move_right()
    elif key == pygame.K_UP:
        game.rotate()
    elif key == pygame.K_DOWN:
        game.soft_drop()
    elif key == pygame.K_SPACE:
        game.hard_drop()
    return True


def handle_event(game, event, held_keys):
    """Обработать одно событие pygame. Возвращает False, если пора выходить.

    held_keys — множество клавиш, которые сейчас зажаты. Оно нужно, чтобы
    отличить настоящее нажатие от автоповтора: пока клавиша зажата, pygame
    снова и снова присылает KEYDOWN. Для стрелок это удобно (фигура едет),
    а для Пробела — нет: иначе зажатый Пробел бросал бы фигуры одну за другой.
    """
    if event.type == pygame.QUIT:
        return False
    if event.type == pygame.KEYUP:
        held_keys.discard(event.key)
        return True
    if event.type != pygame.KEYDOWN:
        return True

    is_repeat = event.key in held_keys
    held_keys.add(event.key)
    if is_repeat and event.key == pygame.K_SPACE:
        return True  # повтор Пробела игнорируем
    return handle_key(game, event.key)


def main():
    """Создать окно и крутить главный цикл, пока игрок не выйдет."""
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Тетрис")
    # Если держать клавишу, она «нажимается» повторно:
    # первый повтор через 170 мс, дальше каждые 50 мс
    pygame.key.set_repeat(170, 50)
    clock = pygame.time.Clock()
    game = Game()
    held_keys = set()  # клавиши, которые сейчас зажаты

    running = True
    while running:
        # clock.tick ждёт, чтобы кадров было не больше FPS,
        # и возвращает, сколько миллисекунд прошло с прошлого кадра
        dt = clock.tick(FPS)

        # 1. События: клавиши и закрытие окна
        for event in pygame.event.get():
            if not handle_event(game, event, held_keys):
                running = False

        # 2. Логика: фигура падает со временем
        game.update(dt)

        # 3. Отрисовка: рисуем кадр и показываем его на экране
        draw(screen, game)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
