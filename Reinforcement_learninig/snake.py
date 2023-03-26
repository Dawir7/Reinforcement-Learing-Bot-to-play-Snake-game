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

            # if keys[pygame.K_LEFT]:
            #     if self.direction_x == 0:
            #         self.direction_x = -1
            #         self.direction_y = 0
            #         self.turns[self.head.position] = [self.direction_x, self.direction_y]
            #
            # elif keys[pygame.K_RIGHT]:
            #     if self.direction_x == 0:
            #         self.direction_x = 1
            #         self.direction_y = 0
            #         self.turns[self.head.position] = [self.direction_x, self.direction_y]
            #
            # elif keys[pygame.K_UP]:
            #     if self.direction_y == 0:
            #         self.direction_x = 0
            #         self.direction_y = -1
            #         self.turns[self.head.position] = [self.direction_x, self.direction_y]
            #
            # elif keys[pygame.K_DOWN]:
            #     if self.direction_y == 0:
            #         self.direction_x = 0
            #         self.direction_y = 1
            #         self.turns[self.head.position] = [self.direction_x, self.direction_y]

        self.move()

    def collision(self, playground, move: tuple[int, int] = (0, 0), add_snack: bool = False) -> tuple[bool, float]:
        reward = 1  # 0 - nothing, +10 - snack, -10 - wall, -8 - himself,
        for count, cube in enumerate(self.body):
            # wall ends game
            if cube.position[0] + move[0] >= playground.rows or cube.position[0] + move[0] < 0:
                reward = -10
                return True, reward
            elif cube.position[1] + move[1] >= playground.rows or cube.position[1] + move[1] < 0:
                reward = -10
                return True, reward
            else:
                for second_cube_count, second_cube in enumerate(self.body):
                    if second_cube_count != count:

                        if second_cube.position[0] + move[1] == cube.position[0] + move[1] and\
                           second_cube.position[1] + move[1] == cube.position[1] + move[1]:  # Hit himself.
                            reward = -8
                            return True, reward

        if self.body[0].position == playground.snack and add_snack:
            playground.pmap[playground.snack] = 0
            self.add_cube()
            playground.score += 1
            reward = 10

        return False, reward

    def move_action(self, action, visual: bool):
        if visual:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        # Action ==> 0 - straight, 1 - left, 2 - right
        if action == 0:
            pass

        elif action == 1:
            self.direction_x, self.direction_y = self.get_left()
            self.turns[self.head.position] = [self.direction_x, self.direction_y]

        elif action == 2:
            self.direction_x, self.direction_y = self.get_right()
            self.turns[self.head.position] = [self.direction_x, self.direction_y]

        self.move()

    def get_left(self):  # ToDo: Maybe we can do it better.
        if self.direction_x == 0 and self.direction_y == 1:
            return 1, 0
        elif self.direction_x == -1 and self.direction_y == 0:
            return 0, 1
        elif self.direction_x == 1 and self.direction_y == 0:
            return 0, -1
        elif self.direction_x == 0 and self.direction_y == -1:
            return -1, 0

    def get_right(self) -> tuple[int, int]:  # ToDo: Maybe we can do it better.
        if self.direction_x == 0 and self.direction_y == 1:
            return -1, 0
        elif self.direction_x == -1 and self.direction_y == 0:
            return 0, -1
        elif self.direction_x == 1 and self.direction_y == 0:
            return 0, 1
        elif self.direction_x == 0 and self.direction_y == -1:
            return 1, 0

    def move_direction(self) -> list[int, int, int, int]:
        # move right, move left, move up, move down
        if self.direction_x == 1:
            return [1, 0, 0, 0]
        elif self.direction_x == -1:
            return [0, 1, 0, 0]
        elif self.direction_y == 1:
            return [0, 0, 0, 1]
        elif self.direction_y == -1:
            return [0, 0, 1, 0]

    def snack_direction(self, playground) -> list[int, int, int, int]:
        # snack right, snack left, snack up, snack down
        if self.body[0].position[0] > playground.snack[0]:
            if self.body[0].position[1] > playground.snack[1]:
                return [0, 1, 1, 0]
            elif self.body[0].position[1] < playground.snack[1]:
                return [0, 1, 0, 1]
            else:
                return [0, 1, 0, 0]
        elif self.body[0].position[0] < playground.snack[0]:
            if self.body[0].position[1] > playground.snack[1]:
                return [1, 0, 1, 0]
            elif self.body[0].position[1] < playground.snack[1]:
                return [1, 0, 0, 1]
            else:
                return [1, 0, 0, 0]
        else:
            if self.body[0].position[1] > playground.snack[1]:
                return [0, 0, 1, 0]
            elif self.body[0].position[1] < playground.snack[1]:
                return [0, 0, 0, 1]
            else:
                return [0, 0, 0, 0]

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
