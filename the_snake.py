import pygame
import random

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость игры
SPEED = 20

class GameObject:
    """
    Базовый класс для игровых объектов.
    """
    def __init__(self, position):
        self.position = position

    def draw(self):
        """
        Абстрактный метод отрисовки объекта.
        """
        pass


class Apple(GameObject):
    """
    Класс яблока.
    """
    def __init__(self):
        super().__init__((0, 0))
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает яблоко в случайное положение на игровом поле.
        """
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, screen):
        """
        Отрисовывает яблоко.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс змейки.
    """
    def __init__(self):
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None

    def move(self):
        """
        Обновляет положение змейки.
        """
        head_x, head_y = self.positions[0]
        move_x, move_y = self.direction
        new_head = (head_x + move_x * GRID_SIZE, head_y + move_y * GRID_SIZE)

        # Добавляем новую голову
        self.positions.insert(0, new_head)
        # Убираем хвост, если длина змейки не увеличивается
        self.positions.pop()

    def grow(self):
        """
        Увеличивает длину змейки.
        """
        self.positions.append(self.positions[-1])

    def update_direction(self):
        """
        Обновляет направление движения змейки.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def check_collision(self):
        """
        Проверяет столкновение с собой.
        """
        head = self.positions[0]
        return head in self.positions[1:]

    def draw(self, screen):
        """
        Отрисовывает змейку.
        """
        for segment in self.positions:
            rect = pygame.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """
    Обрабатывает действия пользователя.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """
    Основная функция игры.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обработка ввода пользователя
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.randomize_position()

        # Проверка столкновения с самим собой
        if snake.check_collision():
            snake = Snake()  # Сброс игры

        # Отрисовка объектов
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
