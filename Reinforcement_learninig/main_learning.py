import pygame
import numpy as np
import pickle
import datetime

from snake import Snake
from map import Map
from agent import Agent

# Version 0.5
MODEL_NAME = "models/model_0v5"  # Name of the pickle file in which we store our model.

# VISUAL = False
# GENERATIONS = 200_000
VISUAL = True
GENERATIONS = 30
MAX_ITERATIONS = 10_000
# epsilon = 1  # epsilon = 0.7 - generation * 0.01
MIN_EPSILON = 0.001
GAMMA = 0.7
LEARNING_RATE = 0.5  # ATTENTION: From model 0v5 this is change dynamically.


def redraw_window(win: pygame.display.set_mode, snake: Snake, playground: Map):
    win.fill((25, 119, 207))
    playground.draw(win)
    snake.draw(win, playground)
    pygame.display.update()  # This updates the screen so we can see our rectangle


def main(visual: bool = True):
    start = datetime.datetime.now()
    best_score = 0
    # MODEL
    try:
        with open(f"{MODEL_NAME}", "rb") as f:
            q_table, generation = pickle.load(f)
    except FileNotFoundError:
        q_table = np.zeros((2 ** 11, 3))
        generation = 0

    # Classes
    agent = Agent()
    playground = Map()
    snake = Snake()
    playground.random_snack_pos(snake)

    # PyGame
    if visual:
        win = pygame.display.set_mode((playground.map_size, playground.map_size))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Snake Game, Generation: 0")

    generations_rewards = []
    generation_time = []

    for gen in range(GENERATIONS):
        generation += 1
        current_state = agent.get_state(snake, playground)
        current_binary_state = agent.make_binary(current_state)

        # It should work as proper reset, but who knows...
        snake.reset()
        playground.pmap[playground.snack] = 0
        playground.score = 0

        # game_over = False
        generation_reward = 0
        iteration = 0
        # epsilon = max(MIN_EPSILON, 0.9 - generation * 0.0008)
        epsilon = max(MIN_EPSILON, 0.9 - generation * 0.000_1)
        LEARNING_RATE = 0.9 - generation * 0.000_004

        if visual:
            pygame.display.set_caption(f"Snake Game, Generation: {generation}")

        for iteration in range(MAX_ITERATIONS):

            if visual:
                clock.tick(30)
                pygame.time.delay(20)
                redraw_window(win, snake, playground)

            # Maybe it can go to agent as get_action.
            # Action ==> 0 - straight, 1 - left, 2 - right
            if np.random.uniform(0, 1) < epsilon:
                action = np.random.randint(3)
            else:
                action = np.argmax(q_table[int(current_binary_state, 2), :])

            snake.move_action(action, visual)
            playground.random_snack_pos(snake)

            # It can be as one function.
            next_state = agent.get_state(snake, playground)
            next_binary_state = agent.make_binary(next_state)
            game_over, reward = snake.collision(playground, add_snack=True)

            bellman_equation = (1 - LEARNING_RATE) * q_table[int(current_binary_state, 2), action] + LEARNING_RATE *\
                               (reward + GAMMA * max(q_table[int(next_binary_state, 2), :]))
            q_table[int(current_binary_state, 2), np.argmax(action)] = bellman_equation

            generation_reward += reward

            if game_over:
                # ToDo: Add some kind of a delay/freeze so we know new generation is coming.
                # print(f"\n\nGAME OVER, GENERATION {generation}, LAST: {iteration} Iterations")
                # print(f"Achieved Score: {playground.score}\n\n")
                if playground.score > best_score:
                    best_score = playground.score
                break

            # current_state = next_state
            current_binary_state = next_binary_state
            if visual:
                print(f"SCORE: {playground.score}")
                print(f"Reward: {reward}, time: {iteration} iterations")

        generations_rewards.append(generation_reward)
        generation_time.append(iteration)
        # print(f"Rewards : {generations_rewards}")
        # print(f"Time : {generation_time}")

    print(f"\nTime of leaning last: {datetime.datetime.now() - start}, for {GENERATIONS} generations.")
    print(f"Best score was: {best_score}")
    print(f"Age: {generation} generations.")

    with open(f"{MODEL_NAME}", "wb") as f:
        data = (q_table, generation)
        pickle.dump(data, f)


if __name__ == "__main__":
    main(VISUAL)
