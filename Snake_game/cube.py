import pygame
from map import Map


class Cube:

    def __init__(self, position):
        self.position = position
        self.direction_x = 1
        self.direction_y = 0

    def move(self):
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, surface, pmap, eyes=False):
        pygame.draw.rect(surface, (0, 255, 0), (self.position[0] * pmap.tail_size + 1,
                                                self.position[1] * pmap.tail_size + 1,
                                                pmap.tail_size - 2, pmap.tail_size - 2))

        if eyes:  # ToDo: Repair hardcodes.
            centre = pmap.tail_size // 2
            radius = 3
            eye_one = (self.position[0] * pmap.tail_size + centre - radius, self.position[1] * pmap.tail_size + 8)
            eye_two = (self.position[0] * pmap.tail_size + pmap.tail_size - radius * 2,
                       self.position[1] * pmap.tail_size + 8)
            pygame.draw.circle(surface, (0, 0, 0), eye_one, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye_two, radius)

