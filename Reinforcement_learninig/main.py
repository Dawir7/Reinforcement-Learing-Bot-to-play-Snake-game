import pygame
from snake import Snake
from map import Map


def redraw_window(win: pygame.display.set_mode, snake: Snake, playground: Map):
    win.fill((25, 119, 207))
    playground.draw(win)
    snake.draw(win, playground)
    pygame.display.update()  # This updates the screen so we can see our rectangle


def main():
    playground = Map()
    win = pygame.display.set_mode((playground.map_size, playground.map_size))

    snake = Snake()
    run = True
    clock = pygame.time.Clock()
    while run:
        # ToDo: Time management.
        clock.tick(30)
        pygame.time.delay(100)
        snake.keyboard_input()
        playground.random_snack_pos(snake)

        if snake.collision(playground):
            print(f"GAME OVER\nSCORE: {playground.score}")
            run = False
            # game_over(win, playground, snake)
            break
        redraw_window(win, snake, playground)


if __name__ == "__main__":
    main()
