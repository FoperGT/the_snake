import pygame
from random import randint

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
SPEED = 20

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


class GameObject:

    def __init__(self, position=(GRID_SIZE * 10, GRID_SIZE * 10),
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):

    def __init__(self, position=(GRID_SIZE * 10, GRID_SIZE * 10)):
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, length=3, position=(GRID_SIZE * 5, GRID_SIZE * 5),
                 body_color=SNAKE_COLOR, direction=RIGHT):
        super().__init__(position, body_color)
        self.length = length
        self.positions = [position]
        for _ in range(length - 1):
            self.positions.append((position[0] - GRID_SIZE, position[1]))
        self.direction = direction
        self.next_direction = None
        self.last = None

    def update_direction(self, direction):
        if direction != self.direction:
            self.next_direction = direction

    def move(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        self.last = self.positions[-1]
        head_x, head_y = self.positions[0]
        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            del self.positions[-1]

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.length = 3


def handle_keys(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.update_direction(UP)
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.update_direction(RIGHT)


def main():
    snake = Snake()
    apple = Apple()
    apple.randomize_position()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.move()
        snake.draw()
        apple.draw()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        head_x, head_y = snake.get_head_position()
        if (head_x < 0 or head_x >= SCREEN_WIDTH
                or head_y < 0 or head_y >= SCREEN_HEIGHT):
            snake.reset()
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
