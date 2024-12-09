from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Все возможные ячейки поля
ALL_CELLS = {(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position, body_color):
        """
        Инициализация игрового объекта.

        :param position: Позиция объекта на игровом поле.
        :param body_color: Цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта на игровом поле."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, snake_positions):
        """Инициализация яблока с случайной позицией, не на теле змейки."""
        free_cells = ALL_CELLS - set(snake_positions)
        position = choice(tuple(free_cells))
        super().__init__(position, APPLE_COLOR)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки с начальной позицией и направлением."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        super().__init__(self.positions[0], SNAKE_COLOR)

    def move(self):
        """Движение змейки в текущем направлении."""
        self.update_direction()
        head = self.positions[0]
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        if new_head in self.positions:
            self.positions = [new_head]
        else:
            self.positions.insert(0, new_head)
            self.last = self.positions.pop()

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовка змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(
            self.positions[0][0] * GRID_SIZE,
            self.positions[0][1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                self.last[0] * GRID_SIZE,
                self.last[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def handle_keys(self):
        """Обработка нажатий клавиш для управления змейкой."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)
    record_size = 0

    while True:
        clock.tick(SPEED)

        snake.handle_keys()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            apple = Apple(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

        if len(snake.positions) > record_size:
            record_size = len(snake.positions)
            pygame.display.set_caption(f'Змейка - Рекорд: {record_size}')


if __name__ == '__main__':
    main()