import pygame
import random

CELL_SIZE = 20
FIELD_WIDTH = 32
FIELD_HEIGHT = 24
SCREEN_WIDTH = CELL_SIZE * FIELD_WIDTH
SCREEN_HEIGHT = CELL_SIZE * FIELD_HEIGHT

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    """Базовый класс игрового объекта с позицией и цветом."""

    def __init__(self, position):
        """
        Инициализирует объект.

        :param position: Кортеж (x, y) позиции на игровом поле.
        """
        self.position = position
        self.body_color = None

    def draw(self, surface):
        """Отрисовка объекта на поверхности surface. Метод должен быть переопределён."""
        pass


class Apple(GameObject):
    """Класс яблока, которое появляется в случайной клетке игрового поля."""

    def __init__(self):
        """Инициализация с назначением случайной позиции и красным цветом."""
        super().__init__((0, 0))
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Установка случайной позиции яблока в пределах игрового поля по клеткам."""
        x = random.randint(0, FIELD_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, FIELD_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле как квадрат нужного цвета."""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки с логикой движения, отрисовки и управления."""

    def __init__(self):
        """Инициализация змейки: одной головой в центре экрана, движущейся вправо."""
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        super().__init__((center_x, center_y))
        self.body_color = GREEN
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)  # движение вправо (в клетках)
        self.next_direction = None

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """
        Обновляет направление движения змейки при условии,
        что новая команда не является противоположной текущему движению.
        """
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Смещает змейку на одну клетку в текущем направлении.
        Если длина змейки не увеличилась (яблоко не съели), удаляется последний сегмент.
        И реализована "телепортация" при выходе за границы поля.
        """
        cur_head = self.get_head_position()
        new_x = (cur_head[0] + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH
        new_y = (cur_head[1] + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        center_x = (FIELD_WIDTH // 2) * CELL_SIZE
        center_y = (FIELD_HEIGHT // 2) * CELL_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = (1, 0)
        self.next_direction = None

    def draw(self, surface):
        """Отрисовывает змейку на игровом поле, закрашивая все сегменты."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш,
    устанавливая следующее направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (1, 0)
    return True


def main():
    """Основной игровой цикл, инициализация, логика, отрисовка и обновления экрана."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона — Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        running = handle_keys(snake)

        snake.update_direction()
        snake.move()

        # Проверка съедения яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Избежание появления яблока внутри змейки
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения змейки с самим собой (все сегменты, кроме головы)
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        # Отрисовка игрового поля и объектов
        screen.fill(BLACK)  # затираем экран
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
