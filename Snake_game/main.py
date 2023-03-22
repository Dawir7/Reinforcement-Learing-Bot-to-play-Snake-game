import pygame
from snake import Snake
from cube import Cube
from map import Map


def keyboard_input(snake: Snake):  # ToDo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if snake.direction_x == 0:
                snake.direction_x = -1
                snake.direction_y = 0
                snake.turns[snake.head.position] = [snake.direction_x, snake.direction_y]

        elif keys[pygame.K_RIGHT]:
            if snake.direction_x == 0:
                snake.direction_x = 1
                snake.direction_y = 0
                snake.turns[snake.head.position] = [snake.direction_x, snake.direction_y]

        elif keys[pygame.K_UP]:
            if snake.direction_y == 0:
                snake.direction_x = 0
                snake.direction_y = -1
                snake.turns[snake.head.position] = [snake.direction_x, snake.direction_y]

        elif keys[pygame.K_DOWN]:
            if snake.direction_y == 0:
                snake.direction_x = 0
                snake.direction_y = 1
                snake.turns[snake.head.position] = [snake.direction_x, snake.direction_y]


def redraw_window(surface):
    pass


def main():
    # width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = Snake()
    # snack = Cube(Map.RandomSnack(rows, s), color=(255, 0, 0))
    run = True
    clock = pygame.time.Clock()
    while run:
        pygame.time.delay(100)
        clock.tick(30)
        snake.move()

        if snake.body[0].position == snack.position:
            snake.add_cube()
            # snack = cube(randomSnack(rows, s), color=(255, 0, 0))

        snake.collision()
        redraw_window(win)
