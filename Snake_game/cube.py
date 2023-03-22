import pygame


class Cube:
    # ToDo: rows, width to map.py (Map)
    rows = 20
    w = 500

    def __init__(self, position):
        self.position = position
        self.direction_x = 1
        self.direction_y = 0

    def move(self):
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # ToDo: pmap.tail_size
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, (0, 255, 0), (self.position[0] * dis + 1, self.position[1] * dis + 1,
                                                dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = 3
            eye_one = (self.position[0] * dis + centre - radius, self.position[1] * dis + 8)
            eye_two = (self.position[0] * dis + dis - radius * 2, self.position[1] * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), eye_one, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye_two, radius)

