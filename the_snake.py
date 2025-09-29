import random
import sys

import pygame as pg

# Константы игры
CELL_SIZE = 20
FIELD_WIDTH = 32
FIELD_HEIGHT = 24
SCREEN_WIDTH = CELL_SIZE * FIELD_WIDTH
SCREEN_HEIGHT = CELL_SIZE * FIELD_HEIGHT

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Изгиб Питона — Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игрового объекта с позицией и цветом."""

    def __init__(self, position=(0, 0), body_color=None):
        """
        Инициализирует объект.

        Args:
            position (tuple): Позиция (x, y) на игровом поле.
            body_color (tuple): Цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта на игровом поле."""
        raise NotImplementedError(
            f'Method draw() not implemented in {self.__class__.__name__}'
        )


class Apple(GameObject):
    """Яблоко, появляется в случайной клетке игрового поля."""

    def __init__(self, occupied_positions=None, body_color=RED):
        """
        Инициализация яблока.

        Args:
            occupied_positions (list): Занятые позиции, где нельзя размещать яблоко.
            body_color (tuple): Цвет яблока.
        """
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию яблока вне занятых клеток."""
        if occupied_positions is None:
            occupied_positions = []

        while True:
            x = random.randint(0, FIELD_WIDTH - 1) * CELL_SIZE
            y = random.randint(0, FIELD_HEIGHT - 1) * CELL_SIZE
            pos = (x, y)
            # Исправлена проверка для соответствия E713
            if pos not in occupied_positions:
                self.position = pos
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(
            self.position[0], self.position[1], CELL_SIZE, CELL_SIZE
        )
        pg.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Змейка с логикой движения, отрисовки и управления."""

    def __init__(self, body_color=GREEN):
        """Инициализация змейки."""
        super().__init__(body_color=body_color)
        self.reset()

    def reset(self):
        """Сброс змейки к начальному положению и длине."""
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        self.length = 1
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """
        Обновляет направление движения.

        Args:
            next_direction (tuple): Следующее направление.
        """
        if next_direction is not None:
            opposite = (-self.direction[0], -self.direction[1])
            if next_direction != opposite:
                self.direction = next_direction

    def move(self):
        """Перемещает змейку на одну клетку вперед."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * CELL_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            tail = self.positions.pop()
            erase_rect = pg.Rect(
                tail[0], tail[1], CELL_SIZE, CELL_SIZE
            )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, erase_rect)

    def draw(self):
        """Отрисовывает змейку на экране."""
        for pos in self.positions:
            rect = pg.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, self.body_color, rect)


def handle_keys():
    """Обрабатывает нажатия клавиш и возвращает направление змейки."""
    next_direction = None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                next_direction = UP
            elif event.key == pg.K_DOWN:
                next_direction = DOWN
            elif event.key == pg.K_LEFT:
                next_direction = LEFT
            elif event.key == pg.K_RIGHT:
                next_direction = RIGHT
    return next_direction


def main():
    """Главная функция игры."""
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        next_dir = handle_keys()
        snake.update_direction(next_dir)
        snake.move()

        head = snake.get_head_position()
        if head == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_positions=snake.positions)
        elif head not in snake.positions[1:]:
            pass
        else:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
