import numpy as np
import pygame


class Map:

    def __init__(self):
        self.rows = 20
        self.map_size = 500
        self.tile_size = self.map_size / self.rows
        self.pmap = np.zeros((self.rows, self.rows))
        self.snack = []

    def draw(self, surface):
        pmap_draw = np.rot90(self.pmap.copy(), 0)
        for i in range(self.rows):
            for j in range(self.rows):
                pygame.draw.line(surface=surface,
                                 color=(0, 0, 0),
                                 start_pos=(i * self.tile_size, j * self.tile_size),
                                 end_pos=(i * self.tile_size, self.rows * self.tile_size))
                pygame.draw.line(surface=surface,
                                 color=(0, 0, 0),
                                 start_pos=(j * self.tile_size, i * self.tile_size),
                                 end_pos=(self.rows * self.tile_size, i * self.tile_size))
        pygame.draw.rect(surface=surface,
                         color=((255, 0, 241)),
                         rect=(self.snack[0] * self.tile_size + 1, self.snack[1] * self.tile_size + 1, self.tile_size - 1, self.tile_size - 1)
                         )

    def random_snack_pos(self, snake):

        if 1 not in self.pmap:
            while True:
                snack_pos = np.random.randint(0, self.rows, 2)
                on_snake = False

                for cube in snake.body:

                    print(cube.position)
                    if snack_pos is cube.position:
                        on_snake = True

                if not on_snake:
                    self.snack = snack_pos
                    self.pmap[snack_pos[0], snack_pos[1]] = 1
                    break
