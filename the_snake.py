import random

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на игровом поле."""
        rect = pg.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое может съесть змейка."""

    def __init__(self, occupied_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию для яблока."""
        if occupied_positions is None:
            occupied_positions = set()
        while True:
            new_position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break


class Snake(GameObject):
    """Змейка, управляемая игроком."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        self.direction = direction

    def move(self):
        """Перемещает змейку на одну клетку вперёд."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % GRID_WIDTH,
            (head_y + dy) % GRID_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for i, position in enumerate(self.positions):
            rect = pg.Rect(
                (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            if i == 0:
                pg.draw.rect(surface, self.body_color, rect)
                pg.draw.rect(surface, BORDER_COLOR, rect, 1)
            else:
                pg.draw.rect(surface, self.body_color, rect)
                pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    next_direction = None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                next_direction = RIGHT
    if next_direction:
        snake.update_direction(next_direction)


def main():
    """Запускает основной цикл игры 'Змейка'."""
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Изгиб Питона — Змейка')
    clock = pg.time.Clock()

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
            apple.randomize_position(occupied_positions=set(snake.positions))

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)

        pg.display.flip()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
