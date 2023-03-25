from cube import Cube
import pygame


class Snake:
    body = []
    turns = {}
    default_position = (1, 10)

    def __init__(self):
        self.head = Cube(self.default_position)
        self.body.append(self.head)
        self.direction_x = 1
        self.direction_y = 0

    def move(self):
        """
        We iterate over the cubes and move them. If in a given position
        the user has made a turn then in that position the cube must
        turn, if it is the last cube then we remove the turn.
        """
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

    def keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                if self.direction_x == 0:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turns[self.head.position] = [self.direction_x, self.direction_y]

            elif keys[pygame.K_RIGHT]:
                if self.direction_x == 0:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.head.position] = [self.direction_x, self.direction_y]

            elif keys[pygame.K_UP]:
                if self.direction_y == 0:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turns[self.head.position] = [self.direction_x, self.direction_y]

            elif keys[pygame.K_DOWN]:
                if self.direction_y == 0:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turns[self.head.position] = [self.direction_x, self.direction_y]

        self.move()

    def collision(self, playground) -> bool:
        for count, cube in enumerate(self.body):
            #  teleport on walls
            '''if cube.position[0] >= playground.rows:
                cube.position = (0, cube.position[1])
            elif cube.position[0] < 0:
                cube.position = (playground.rows, cube.position[1])
            elif cube.position[1] >= playground.rows:
                cube.position = (cube.position[0], 0)
            elif cube.position[1] < 0:
                cube.position = (cube.position[0], playground.rows)'''

            # wall ends game
            if cube.position[0] >= playground.rows or cube.position[0] < 0:
                return True
            elif cube.position[1] >= playground.rows or cube.position[1] < 0:
                return True
            else:
                for second_cube_count, second_cube in enumerate(self.body):
                    if second_cube_count != count:
                        if second_cube.position == cube.position:  # Hit himself.
                            return True

        if self.body[0].position == playground.snack:
            playground.pmap[playground.snack] = 0
            self.add_cube()
            playground.score += 1

        return False

    def reset(self):
        self.head = Cube(self.default_position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 1
        self.direction_y = 0

    def add_cube(self):
        tail = self.body[-1]
        direction_x, direction_y = tail.direction_x, tail.direction_y
        # We are checking in which site of tail add cube at the end of the snake.
        if direction_x == 1 and direction_y == 0:
            self.body.append(Cube((tail.position[0] - 1, tail.position[1])))
        elif direction_x == -1 and direction_y == 0:
            self.body.append(Cube((tail.position[0] + 1, tail.position[1])))
        elif direction_x == 0 and direction_y == 1:
            self.body.append(Cube((tail.position[0], tail.position[1] - 1)))
        elif direction_x == 0 and direction_y == -1:
            self.body.append(Cube((tail.position[0], tail.position[1] + 1)))

        self.body[-1].direction_x = direction_x
        self.body[-1].direction_y = direction_y

    def draw(self, surface: pygame.display.set_mode, playground):
        for iteration, cube in enumerate(self.body):
            if iteration == 0:
                cube.draw(surface, playground, True)  # Head -> body with eyes
            else:
                cube.draw(surface, playground)
