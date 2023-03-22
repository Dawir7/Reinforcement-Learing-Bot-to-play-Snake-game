import pygame


class Cube:
    # ToDo: rows, width to map.py (Map)
    rows = 20
    w = 500

    def __init__(self, position):
        self.position = position
        self.directory_x = 1
        self.directory_y = 0

    def move(self):
        self.position = (self.position[0] + self.directory_x, self.position[1] + self.directory_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, (0, 255, 0), (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = 3
            eye_one = (i * dis + centre - radius, j * dis + 8)
            eye_two = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), eye_one, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye_two, radius)

