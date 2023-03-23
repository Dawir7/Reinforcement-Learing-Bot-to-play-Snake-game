import numpy as np
import pygame


class Map:

    def __init__(self):
        self.rows = 20
        self.map_size = 500
        self.tile_size = self.map_size / self.rows
        self.pmap = np.zeros((self.rows, self.rows))

    def draw(self, playground):

        for i in range(self.rows):
            for j in range(self.rows):
                pygame.draw.line(surface=playground,
                                 color=(0, 0, 0),
                                 start_pos=(i * self.tile_size, j * self.tile_size),
                                 end_pos=(i * self.tile_size, self.rows * self.tile_size))
                pygame.draw.line(surface=playground,
                                 color=(0, 0, 0),
                                 start_pos=(j * self.tile_size, i * self.tile_size),
                                 end_pos=(self.rows * self.tile_size, i * self.tile_size))

    def random_snack(self, snake):

        while True:
            snack_pos = np.random.randint(0, self.rows, 2)
            on_snake = False

            for cube in snake.body:
                if snack_pos == cube.position:
                    on_snake = True

            if not on_snake:
                self.pmap[snack_pos[0], snack_pos[1]] = 1
                break


# def main():  # just for checking if that class works fine
#     mapa = Map()
#     print(mapa.pmap)
#
#
# if __name__ == "__main__":
#     main()
