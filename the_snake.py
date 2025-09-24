import sys
import random
import warnings

# Отключаем все предупреждения Python
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
    """Базовый класс игрового объекта."""

    def __init__(self, position):
        """Инициализирует игровой объект.

        Args:
            position (tuple): координаты объекта.
        """
        self.position = position
        self.body_color = None

    def draw(self, surface):
        """Отрисовка объекта."""
        pass


class Apple(GameObject):
    """Яблоко, которое появляется в случайной позиции."""

    def __init__(self):
        """Создает яблоко с красным цветом и случайной позицией."""
        super().__init__((0, 0))
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом устанавливает позицию яблока."""
        x = random.randint(0, FIELD_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, FIELD_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Рисует яблоко как квадрат нужного цвета."""
        rect = pygame.Rect(self.position[0],
                           self.position[1],
                           CELL_SIZE,
                           CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки посередине игрового поля."""
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
        """Обновляет направление змейки, не позволяя разворачиваться задом."""
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку, телепортируя через границы."""
        cur_head = self.get_head_position()
        new_x = (cur_head[0] + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH
        new_y = (cur_head[1] + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        self.length = 1
        self.positions = [(center_x, center_y)]
        self.direction = (1, 0)
        self.next_direction = None

    def draw(self, surface):
        """Рисует сегменты змейки."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
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

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
