
class Agent:
    def __init__(self):
        self.amount_of_games = 0
        self.epsilon = 90
        self.gamma = 0.8
        self.data = []  # Maybe better numpy array.

    def get_state(self, snake, playground) -> list:
        """
        state = [danger straight, danger left, danger right, move right, move left,
                 move up, move down, snack right, snack left, snack up, snack down]
        :param snake:
        :param playground:
        :return:
        """
        state = []

        straight = (snake.direction_x, snake.direction_y)
        state.append(int(snake.colision(playground, straight)))
        left = snake.get_left()
        state.append(int(snake.colision(playground, left)))
        right = snake.get_right()
        state.append(int(snake.colision(playground, right)))

        directions = snake.move_direction()
        for direction in directions:
            state.append(direction)

        snack_directions = snake.snack_direction()
        for snack_direction in snack_directions:
            state.append(snack_direction)

        return state

