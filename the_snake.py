import random
import sys

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
    """Базовый класс игрового объекта с позицией и цветом."""

    def __init__(self, position):
        """Инициализирует объект.

        Args:
            position (tuple): Кортеж (x, y) позиции на игровом поле.
        """
        self.position = position
        self.body_color = None

    def draw(self, surface):
        """Отрисовка объекта на поверхности surface."""
        pass


class Apple(GameObject):
    """Яблоко, появляется в случайной клетке игрового поля."""

    def __init__(self):
        """Инициализация с цветом и случайной позицией."""
        super().__init__((0, 0))
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        x = random.randint(0, FIELD_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, FIELD_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле в виде квадрата нужного цвета."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Змейка с логикой движения, отрисовки и управления."""

    def __init__(self):
        """Инициализация змейки в центре игрового поля, движение вправо."""
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        super().__init__((center_x, center_y))
        self.body_color = GREEN
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения, запрещая разворот на 180 градусов."""
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку вперед с телепортацией
