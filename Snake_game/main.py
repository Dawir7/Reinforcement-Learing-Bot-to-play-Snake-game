import pygame
from snake import Snake
from map import Map


def redraw_window(win: pygame.display.set_mode, snake: Snake, playground: Map):
    win.fill((25, 119, 207))
    playground.draw(win)
    snake.draw(win, playground)
    pygame.display.update()  # This updates the screen so we can see our rectangle


# ToDo: Do we need this game over window?
# def game_over(win: pygame.display.set_mode, playground: Map, snake: Snake):
#     """
#         Function responsible for creating a "Game over" window after collision with non-edible ghost
#         :param: win: instance of pygame window (pygame.display.set_mode)
#     """
#     pygame.font.init()
#     win.fill((0, 0, 0))
#     font = pygame.font.SysFont('ComicSans', 40)
#     title = font.render('Game Over', True, (255, 255, 255))
#     restart_button = font.render('R - Restart', True, (255, 255, 255))
#     score = font.render(f'Score: {playground.score}', True, (255, 255, 255))
#     show = True
#     while show:
#         win.blit(title, (playground.map_size / 2 - title.get_width() / 2,
#                          playground.map_size / 4 - title.get_height() / 3))
#         win.blit(restart_button, (playground.map_size / 2 - restart_button.get_width() / 2,
#                                   playground.map_size / 2 - restart_button.get_height() / 2))
#         win.blit(score, (playground.map_size / 2 - score.get_width() / 2,
#                          playground.map_size * 3 / 4 - score.get_height() / 2))
#         reset = snake.keyboard_input()
#         if reset:
#             playground.score = 0
#             playground.pmap[playground.snack] = 0
#         pygame.display.update()


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
