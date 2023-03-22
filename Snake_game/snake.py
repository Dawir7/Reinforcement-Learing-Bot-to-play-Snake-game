import pygame


class Snake:
    body = []
    turns = {}

    def __init__(self, cube, position):
        self.head = cube(position)
        self.body.append(self.head)
        self.directory_x = 0
        self.directory_y = 1

    def move(self):
        # Lecimy po wszystkich kostkach i ruszamy je odpowiednio.
        for iteration, cube in enumerate(self.body):
            position = cube.position[:]  # ???

            # Jeśli w danej pozycji użytkownik dokonał skrętu to w niej kostka musi skręcić,
            # jeśli to ostatni kostka usuwamy zakręt.
            if position in self.turns:
                turn = self.turns[position]
                cube.directory_x = turn[0]
                cube.directory_y = turn[1]
                cube.move()
                if iteration == len(self.body) - 1:
                    self.turns.pop(position)
            # Patrzymy czy to sciana, jesli tak tepamy, inaczej robimy krok o kostkę w dobrą stronę.
            else:
                if cube.directory_x == -1 and cube.position[0] <= 0:  # Transport z lewej ściany mapy.
                    cube.position = (cube.rows - 1, cube.position[1])
                elif cube.directory_x == 1 and cube.position[0] >= cube.rows - 1:  # Transport z prawej ściany mapy.
                    cube.position = (0, cube.position[1])
                elif cube.directory_y == 1 and cube.position[1] >= cube.rows - 1:  # Transport z dołu mapy.
                    cube.position = (cube.position[0], 0)
                elif cube.directory_y == -1 and cube.position[1] <= 0:  # Transport z góry mapy.
                    cube.position = (cube.position[0], cube.rows - 1)
                else:
                    cube.move()  # Normalne przemieszczenie.

    def collision(self):
        pass

    def reset(self, cube, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directory_x = 0
        self.directory_y = 1

    def add_cube(self, cube):
        tail = self.body[-1]
        directory_x, directory_y = tail.directory_x, tail.directory_y
        # We are checking in which site of tail add cube at the end of the snake.
        if directory_x == 1 and directory_y == 0:
            self.body.append(cube((tail.position[0] - 1, tail.position[1])))
        elif directory_x == -1 and directory_y == 0:
            self.body.append(cube((tail.position[0] + 1, tail.position[1])))
        elif directory_x == 0 and directory_y == 1:
            self.body.append(cube((tail.position[0], tail.position[1] - 1)))
        elif directory_x == 0 and directory_y == -1:
            self.body.append(cube((tail.position[0], tail.position[1] + 1)))

        self.body[-1].directory_x = directory_x
        self.body[-1].directory_y = directory_y

    def draw(self, surface):
        for iteration, cube in enumerate(self.body):
            if iteration == 0:
                cube.draw(surface, True)  # Head -> body with eyes
            else:
                cube.draw(surface)
