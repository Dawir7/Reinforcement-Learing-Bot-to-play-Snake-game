import pygame


class Snake:
    body = []
    turns = {}

    def __init__(self, cube, position):
        self.head = cube(position)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1

    def move(self):
        # Lecimy po wszystkich kostkach i ruszamy je odpowiednio.
        for iteration, cube in enumerate(self.body):
            position = cube.position[:]  # ???

            # Jeśli w danej pozycji użytkownik dokonał skrętu to w niej kostka musi skręcić,
            # jeśli to ostatni kostka usuwamy zakręt.
            if position in self.turns:
                turn = self.turns[position]
                cube.direction_x = turn[0]
                cube.direction_y = turn[1]
                cube.move()
                if iteration == len(self.body) - 1:
                    self.turns.pop(position)
            else:
                cube.move()  # Normalne przemieszczenie.

    def collision(self) -> bool:
        for cube in self.body:
            if cube.direction_x == -1 and cube.position[0] <= 0:  # Transport z lewej ściany mapy.
                return True
            elif cube.direction_x == 1 and cube.position[0] >= cube.rows - 1:  # Transport z prawej ściany mapy.
                return True
            elif cube.direction_y == 1 and cube.position[1] >= cube.rows - 1:  # Transport z dołu mapy.
                return True
            elif cube.direction_y == -1 and cube.position[1] <= 0:  # Transport z góry mapy.
                return True
            else:
                for other_cube in self.body:
                    if other_cube.position == cube.position:
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

    def draw(self, surface):
        for iteration, cube in enumerate(self.body):
            if iteration == 0:
                cube.draw(surface, True)  # Head -> body with eyes
            else:
                cube.draw(surface)
