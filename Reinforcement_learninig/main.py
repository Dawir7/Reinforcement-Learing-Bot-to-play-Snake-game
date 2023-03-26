import pygame
import numpy as np
from snake import Snake
from map import Map
from agent import Agent

# Version 0.1


def redraw_window(win: pygame.display.set_mode, snake: Snake, playground: Map):
    win.fill((25, 119, 207))
    playground.draw(win)
    snake.draw(win, playground)
    pygame.display.update()  # This updates the screen so we can see our rectangle


# def main():
#     playground = Map()
#     win = pygame.display.set_mode((playground.map_size, playground.map_size))
#
#     snake = Snake()
#     run = True
#     clock = pygame.time.Clock()
#     while run:
#         # ToDo: Time management.
#         clock.tick(30)
#         pygame.time.delay(100)
#         snake.keyboard_input()
#         playground.random_snack_pos(snake)
#
#         if snake.collision(playground):
#             print(f"GAME OVER\nSCORE: {playground.score}")
#             run = False
#             # game_over(win, playground, snake)
#             break
#         redraw_window(win, snake, playground)


def main():
    # MODEL
    q_table = np.zeros((2 ** 11, 3))
    generations = 100
    max_iterations = 10_000
    # epsilon = 1  # epsilon = 0.7 - generation * 0.01
    min_epsilon = 0.001
    gamma = 0.5
    learning_rate = 0.7

    # Classes
    agent = Agent()
    playground = Map()
    snake = Snake()
    playground.random_snack_pos(snake)

    # PyGame
    win = pygame.display.set_mode((playground.map_size, playground.map_size))
    clock = pygame.time.Clock()

    generations_rewards = []
    generation_time = []

    for generation in range(generations):
        current_state = agent.get_state(snake, playground)
        current_binary_state = agent.make_binary(current_state)

        # It should work as proper reset, but who knows...
        snake.reset()
        playground.pmap[playground.snack] = 0

        # game_over = False
        generation_reward = 0
        iteration = 0

        for iteration in range(max_iterations):

            clock.tick(30)
            pygame.time.delay(100)
            redraw_window(win, snake, playground)

            epsilon = max(min_epsilon, 0.7 - generation * 0.01)
            # Maybe it can go to agent as get_action.
            # Action ==> 0 - straight, 1 - left, 2 - right
            if np.random.uniform(0, 1) < epsilon:
                action = np.random.randint(3)
            else:
                action = np.argmax(q_table[int(current_binary_state, 2), :])

            snake.move_action(action)
            playground.random_snack_pos(snake)

            # It can be as one function.
            next_state = agent.get_state(snake, playground)
            next_binary_state = agent.make_binary(next_state)
            game_over, reward = snake.collision(playground, add_snack=True)

            bellman_equation = (1 - learning_rate) * q_table[int(current_binary_state, 2), action] + learning_rate *\
                               (reward + gamma * max(q_table[int(next_binary_state, 2), :]))
            q_table[int(current_binary_state, 2), np.argmax(action)] = bellman_equation

            generation_reward += reward

            if game_over:
                # ToDo: Add some kind of a delay/freeze so we know new generation is coming.
                print(f"\n\nGAME OVER, GENERATION {generation}, LAST: {iteration} Iterations")
                print(f"Achieved Score: {playground.score}\n\n")
                break

            # current_state = next_state
            current_binary_state = next_binary_state
            print(f"SCORE: {playground.score}")
            print(f"Reward: {reward}, time: {iteration} iterations")

        generations_rewards.append(generation_reward)
        generation_time.append(iteration)
        print(f"Rewards : {generations_rewards}")
        print(f"Time : {generation_time}")


if __name__ == "__main__":
    main()
