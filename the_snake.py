from random import choice, randint

import pygame as pg

# Типы для аннотаций
Pointer = tuple[int, int]
Color = tuple[int, int, int]

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
CENTER: Pointer = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)
DIRECTIONS: list[Pointer] = [UP, DOWN, LEFT, RIGHT]

# Цвета:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)
BORDER_COLOR: Color = (93, 216, 228)
APPLE_COLOR: Color = (255, 0, 0)
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость движения:
SPEED: int = 10

# Инициализация Pygame:
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс для игровых объектов.
    Атрибуты:
        position: позиция объекта (по умолчанию в центре).
        body_color: цвет тела объекта.
    """

    def __init__(
        self,
        position: Pointer = CENTER,
        body_color: Color = BOARD_BACKGROUND_COLOR
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Метод для отрисовки объекта. 
        Должен быть переопределен в наследниках."""
        raise NotImplementedError('Subclasses must implement draw')


class Apple(GameObject):
    """
    Описывает яблоко.
    Атрибуты:
        body_color: цвет яблока.
        position: случайная позиция, не на теле змейки.
    """

    def __init__(self, positions: list[Pointer]) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(positions)

    def randomize_position(self, occupied_positions: list[Pointer]) -> None:
        """Устанавливает случайную позицию яблока, не совпадающую с занятой."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Описывает змейку.
    Атрибуты:
        length: длина змейки.
        positions: список позиций сегментов тела.
        direction: текущее направление движения.
        next_direction: следующее направление (для смены на следующем шаге).
        last: последний сегмент, который был удален после движения.
    """

    def __init__(self) -> None:
        super().__init__(position=CENTER, body_color=SNAKE_COLOR)
        self.length: int = 1
        self.positions = [self.position]
        self.direction: Pointer = RIGHT
        self.next_direction: Pointer | None = None
        self.last: Pointer | None = None

    def update_direction(self) -> None:
        """Обновляет направление движения, если задано новое."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки, учитывая выход за границы экрана."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        # Удаляем последний сегмент, если змейка не растёт
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовывает змейку на экране."""
        for i, pos in enumerate(self.positions):
            rect = pg.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

            # Выделяем голову
            if i == 0:
                pg.draw.rect(screen, (0, 100, 0), rect, 1)

        # Затираем последний сегмент, если он был
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> Pointer:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice(DIRECTIONS)
        self.next_direction = None
        self.last = None


def handle_keys(game_object: Snake) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция игры."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
