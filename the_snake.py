import sys
import random
import warnings

warnings.filterwarnings('ignore')

import pygame


CELL_SIZE = 20
FIELD_WIDTH = 32
FIELD_HEIGHT = 24
SCREEN_WIDTH = CELL_SIZE * FIELD_WIDTH
SCREEN_HEIGHT = CELL_SIZE * FIELD_HEIGHT

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position):
        """
        Инициализирует игровой объект.

        Args:
            position (tuple): координаты объекта.
        """
        self.position = position
        self.body_color = None

    def draw(self, surface):
        """Отрисовка объекта."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко с красным цветом и случайной позицией."""
        super().__init__((0, 0))
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        x = random.randint(0, FIELD_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, FIELD_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Рисует яблоко на экране."""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки посередине экрана."""
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        super().__init__((center_x, center_y))
        self.body_color = GREEN
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """
        Обновляет направление движения,
        предотвращая разворот на 180 градусов.
        """
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку, реализуя эффект телепортации через границы."""
        cur_head = self.get_head_position()
        new_x = (cur_head[0] + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH
        new_y = (cur_head[1] + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное положение и состояние."""
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        self.length = 1
        self.positions = [(center_x, center_y)]
        self.direction = (1, 0)
        self.next_direction = None

    def draw(self, surface):
        """Рисует все сегменты змейки."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """
    Обрабатывает события клавиатуры.

    Args:
        snake (Snake): объект змейки для управления.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (1, 0)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона — Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
