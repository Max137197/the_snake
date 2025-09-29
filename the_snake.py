import random
import sys
import pygame as pg  # принято сокращение для pygame


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


class GameObject:
    """Базовый класс игрового объекта с позицией и цветом."""

    def __init__(self, position=(0, 0), body_color=None):
        """Инициализирует объект.

        Args:
            position (tuple): Кортеж (x, y) позиции на игровом поле.
            body_color (tuple): Цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта на глобальной поверхности screen."""
        raise NotImplementedError(
            f'Метод draw не реализован в классе {self.__class__.__name__}'
        )


class Apple(GameObject):
    """Яблоко, появляется в случайной клетке игрового поля вне змейки."""

    def __init__(self, occupied_positions=None, body_color=RED):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию яблока, не попадающую в занятые клетки."""
        if occupied_positions is None:
            occupied_positions = set()
        while True:
            x = random.randint(0, FIELD_WIDTH - 1) * CELL_SIZE
            y = random.randint(0, FIELD_HEIGHT - 1) * CELL_SIZE
            pos = (x, y)
            if pos not in occupied_positions:
                self.position = pos
                break

    def draw(self):
        rect = pg.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pg.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Змейка с логикой движения, отрисовки и управления."""

    def __init__(self, body_color=GREEN):
        self.reset()
        super().__init__(position=self.positions[0], body_color=body_color)

    def reset(self):
        """Сбрасывает змейку к начальному положению и длине."""
        self.length = 1
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Обновляет направление движения без поворота назад."""
        if next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if next_direction != opposite:
                self.direction = next_direction

    def move(self):
        """Перемещает змейку вперед на одну клетку с обработкой выхода за границы экрана."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * CELL_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает все сегменты змейки на игровом поле."""
        for pos in self.positions:
            rect = pg.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, self.body_color, rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш, управляя направлением змейки."""
    next_dir = None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                next_dir = UP
            elif event.key == pg.K_DOWN:
                next_dir = DOWN
            elif event.key == pg.K_LEFT:
                next_dir = LEFT
            elif event.key == pg.K_RIGHT:
                next_dir = RIGHT
    if next_dir:
        snake.update_direction(next_dir)


# Инициализация pygame и глобальная поверхность для рисования
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Изгиб Питона — Змейка')
clock = pg.time.Clock()


def main():
    """Основной цикл игры: обновление и отрисовка объектов."""
    snake = Snake()
    apple = Apple(occupied_positions=set(snake.positions))

    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_positions=set(snake.positions))

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pg.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
