import pygame
from snake import Snake
from cube import Cube
from map import Map

# ToDo:
# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         pygame.quit()
#         quit()
#
#     keys = pygame.key.get_pressed()
#     for key in keys:
#         if keys[pygame.K_LEFT]:
#             if not self.right:
#                 self.left = True
#                 self.right = False
#                 self.down = False
#                 self.up = False
#                 self.dirnx = -1
#                 self.dirny = 0
#                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
#             else:
#                 pass
#
#         elif keys[pygame.K_RIGHT]:
#             if not self.left:
#                 self.left = False
#                 self.right = True
#                 self.down = False
#                 self.up = False
#                 self.dirnx = 1
#                 self.dirny = 0
#                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
#             else:
#                 pass
#
#         elif keys[pygame.K_UP]:
#             if not self.down:
#                 self.left = False
#                 self.right = False
#                 self.down = False
#                 self.up = True
#                 self.dirnx = 0
#                 self.dirny = -1
#                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
#             else:
#                 pass
#
#         elif keys[pygame.K_DOWN]:
#             if not self.up:
#                 self.left = False
#                 self.right = False
#                 self.down = True
#                 self.up = False
#                 self.dirnx = 0
#                 self.dirny = 1
#                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
#             else:
#                 pass


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
