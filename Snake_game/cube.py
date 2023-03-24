import pygame
from map import Map


class Cube:

    def __init__(self, position):
        self.position = position
        self.direction_x = 1
        self.direction_y = 0

    def move(self):
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, surface, playground, eyes=False):
        pygame.draw.rect(surface, (47, 199, 16), (self.position[0] * playground.tile_size + 1,
                                                self.position[1] * playground.tile_size + 1,
                                                playground.tile_size - 2, playground.tile_size - 2))

        if eyes:  # ToDo: Repair hardcodes.
            centre = playground.tile_size // 2
            radius = 3
            eye_one = (self.position[0] * playground.tile_size + centre - radius,
                       self.position[1] * playground.tile_size + 8)
            eye_two = (self.position[0] * playground.tile_size + playground.tile_size - radius * 2,
                       self.position[1] * playground.tile_size + 8)
            pygame.draw.circle(surface, (0, 0, 0), eye_one, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye_two, radius)
