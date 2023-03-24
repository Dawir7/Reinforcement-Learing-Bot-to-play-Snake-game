import pygame
from cube import Cube


class Snake:
    body = []
    turns = {}

    def __init__(self, position):
        self.head = Cube(position)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1

    def move(self):  # ToDo: Repair
        # We are iterating through a cubes and move them.
        # Jeśli w danej pozycji użytkownik dokonał skrętu to w niej kostka musi skręcić,
        # jeśli to ostatni kostka usuwamy zakręt.
        for iteration, cube in enumerate(self.body):
            if cube.position in self.turns.keys():
                turn = self.turns[cube.position]
                cube.direction_x = turn[0]
                cube.direction_y = turn[1]
                if iteration == len(self.body) - 1:
                    self.turns.pop(cube.position)
                cube.move()
            else:
                cube.move()

    def collision(self, playground) -> bool:
        for cube in self.body:
            # if cube.direction_x == -1 and cube.position[0] <= 0:  # Hit the left wall.
            #     return True
            # elif cube.direction_x == 1 and cube.position[0] >= cube.rows - 1:  # Hit the right wall.
            #     return True
            # elif cube.direction_y == 1 and cube.position[1] >= cube.rows - 1:  # Hit the bottom.
            #     return True
            # elif cube.direction_y == -1 and cube.position[1] <= 0:  # Hit the celling.
            #     return True
            if cube.position[0] >= playground.rows or cube.position[0] <= 0:
                return True
            elif cube.position[1] >= playground.rows or cube.position[1] <= 0:
                return True
            else:
                for other_cube in self.body:
                    if cube != cube:
                        if other_cube.position == cube.position:  # Hit himself.
                            return True

        return False

    def reset(self, cube, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1

    def add_cube(self, cube):
        tail = self.body[-1]
        direction_x, direction_y = tail.direction_x, tail.direction_y
        # We are checking in which site of tail add cube at the end of the snake.
        if direction_x == 1 and direction_y == 0:
            self.body.append(cube((tail.position[0] - 1, tail.position[1])))
        elif direction_x == -1 and direction_y == 0:
            self.body.append(cube((tail.position[0] + 1, tail.position[1])))
        elif direction_x == 0 and direction_y == 1:
            self.body.append(cube((tail.position[0], tail.position[1] - 1)))
        elif direction_x == 0 and direction_y == -1:
            self.body.append(cube((tail.position[0], tail.position[1] + 1)))

        self.body[-1].direction_x = direction_x
        self.body[-1].direction_y = direction_y

    def draw(self, surface, playground):
        for iteration, cube in enumerate(self.body):
            if iteration == 0:
                cube.draw(surface, playground, True)  # Head -> body with eyes
            else:
                cube.draw(surface, playground)
