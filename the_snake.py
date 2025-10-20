from random import choice, randint

import pygame as pg

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Color = (255, 0, 0)

# Цвет по умолчанию
DEFAULT_COLOR: Color = (0, 0, 0)

# Цвет змейки
SNAKE_COLOR: Color = (0, 255, 0)

# Начальная позиция змейки по центру
SNAKE_POSITION: list[Pointer] = [CENTER]

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс.
    Атрибуты:
        position — расположена в центре экрана.
        body_color — цвет объекта по умолчанию.
    Метод draw предназначен для переопределения в подклассах.
    """

    def __init__(self, body_color: Color = DEFAULT_COLOR) -> None:
        self.position: Pointer = CENTER
        self.body_color: Color = body_color

    def draw(self) -> None:
        """Метод для переопределения в дочерних классах."""
        ...


class Apple(GameObject):
    """Описывает появление яблока, наследуется от GameObject.
    Атрибуты:
        body_color — равен цвету яблока.
        position — вычисляется случайно с помощью randomize_position.
    Методы:
        randomize_position — устанавливает случайную позицию.
        draw — отрисовывает яблоко.
    """

    def __init__(
        self,
        body_color: Color = APPLE_COLOR,
        positions: list[Pointer] = None
    ) -> None:
        super().__init__(body_color=body_color)
        if positions is None:
            positions = SNAKE_POSITION
        self.randomize_position(positions)

    def randomize_position(self, positions: list[Pointer]) -> None:
        """Устанавливает случайную позицию яблока."""
        while True:
            random_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if random_position not in positions:
                break
        self.position = random_position

    def draw(self) -> None:
        """Рисует яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает поведение змейки, наследуется от GameObject.
    Атрибуты:
        length — длина змейки, равна 1.
        positions — список позиций всех сегментов тела.
        direction — текущее направление движения.
        next_direction — следующее направление после нажатия клавиши.
        body_color — цвет змейки.
        last — последний сегмент (для затирания).
    Методы:
        update_direction — обновляет направление.
        move — обновляет позицию змейки.
        draw — отрисовывает змейку.
        get_head_position — возвращает позицию головы.
        reset — сбрасывает змейку в начальное состояние.
    """

    def __init__(self) -> None:
        super().__init__()
        self.length: int = 1
        self.positions: list[Pointer] = [CENTER]
        self.direction: Pointer = RIGHT
        self.next_direction: Pointer | None = None
        self.body_color: Color = SNAKE_COLOR
        self.last: Pointer | None = None

    def update_direction(self) -> None:
        """Обновляет направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки с учётом перехода через границы."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовывает змейку на экране."""
        # Отрисовка тела
        for position in self.positions[1:]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание хвоста (если он есть)
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
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object: Snake) -> None:
    """Обрабатывает нажатия клавиш."""
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
    pg.init()
    snake = Snake()
    apple = Apple(positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        # Проверка на столкновение с собой
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
