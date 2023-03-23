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


def redraw_window(win, snake, playground):
    win.fill((255, 255, 255))
    playground.draw(win)
    snake.draw(win, playground)
    pygame.display.update()  # This updates the screen so we can see our rectangle


def main():
    playground = Map()
    win = pygame.display.set_mode((playground.map_size, playground.map_size))

    snake = Snake((0, 10))
    # snack = Cube(Map.RandomSnack(rows, s), color=(255, 0, 0))
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        pygame.time.delay(100)
        keyboard_input(snake)
        snake.move()

        # if snake.body[0].position == snack.position:
        #     snake.add_cube()
        # snack = cube(randomSnack(rows, s), color=(255, 0, 0))

        # snake.collision()
        redraw_window(win, snake, playground)


if __name__ == "__main__":
    main()
