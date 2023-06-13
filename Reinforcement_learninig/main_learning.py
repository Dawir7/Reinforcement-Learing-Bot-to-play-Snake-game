import pygame
import numpy as np
import pickle
import datetime
import os
from snake import Snake
from map import Map
from agent import Agent

# Version 1.1
MODEL_DIR = "models"
MODEL_NAME = "model_1v7"  # Name of the pickle file in which we store our model.
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)
# MODEL_NAME = "models/Best_model"  # Name of the pickle file in which we store our model.

GATHER_DATA = True
DATA_DIR = r"..\data"
DATA_PATH = os.path.join(DATA_DIR, f"data_{MODEL_NAME}_dis")

learn = 1
if learn:
    VISUAL = False
    GENERATIONS = 50
    save = False
    epsilon_dec = 0.000_03
else:
    VISUAL = True
    GENERATIONS = 30
    save = False
    epsilon_dec = 0.1


MAX_ITERATIONS = 7_000  # max iterations in game # Dropped to 5_000!!!
MIN_EPSILON = 0.0001

epsilon_dec = 0.1
GAMMA = 0.4
LEARNING_RATE = 0.2
MIN_LEARNING_RATE = 0.3


def redraw_window(win: pygame.display.set_mode, snake: Snake, playground: Map):
    win.fill((25, 119, 207))
    playground.draw(win)
    snake.draw(win, playground)
    pygame.display.update()  # This updates the screen so we can see our rectangle


def main(visual: bool = True):
    start = datetime.datetime.now()
    st2 = datetime.datetime.now()
    best_score = 0
    best_time = 0
    # MODEL
    if os.path.isfile(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            q_table, generation = pickle.load(f)
    else:
        if not os.path.isdir(MODEL_DIR):
            os.mkdir(MODEL_DIR)
        q_table = np.zeros((2 ** 11, 3))
        generation = 0

    if os.path.isfile(DATA_PATH):
        with open(DATA_PATH, 'rb') as f:
            gameplay_data = pickle.load(f)
    else:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        gameplay_data = []

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
        playground.reset()

        # game_over = False
        generation_reward = 0
        iteration = 0
        # epsilon = max(MIN_EPSILON, 0.9 - generation * 0.0008)
        epsilon = max(MIN_EPSILON, 0.9 - generation * epsilon_dec)
        # LEARNING_RATE = max(0.95 - generation * 0.000_000_004, MIN_LEARNING_RATE)

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
                probability = max(q_table[int(current_binary_state, 2), :])

            if GATHER_DATA:
                gameplay_data.append([current_state, probability])

            snake.move_action(action, visual)
            playground.random_snack_pos(snake)

            # It can be as one function.
            next_state = agent.get_state(snake, playground)
            next_binary_state = agent.make_binary(next_state)
            game_over, reward = snake.collision(playground, add_snack=True)

            bellman_equation = (1 - LEARNING_RATE) * q_table[int(current_binary_state, 2), action] + LEARNING_RATE *\
                               (reward + GAMMA * max(q_table[int(next_binary_state, 2), :]))
            # bellman_equation = max(q_table[int(next_binary_state, 2), :]) + LEARNING_RATE * (reward + GAMMA + (
            #             max(q_table[int(next_binary_state, 2), :]) - q_table[int(current_binary_state, 2), action]))
            q_table[int(current_binary_state, 2), action] = bellman_equation

            generation_reward += reward

            if game_over:
                if playground.score > best_score:
                    best_score = playground.score
                    if best_score > 10 and save:
                        with open(f"models/Best_model", "wb") as f:
                            data = (q_table, generation)
                            pickle.dump(data, f)
                if iteration > best_time:
                    best_time = iteration
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
        if generation % 100 == 0:
            print(generation, datetime.datetime.now() - st2, best_score, best_time)
            if save:
                with open(MODEL_PATH, "wb") as f:
                    data = (q_table, generation)
                    pickle.dump(data, f)
            if GATHER_DATA:
                with open(DATA_PATH, "wb") as f:
                    pickle.dump(gameplay_data, f)
            st2 = datetime.datetime.now()

    print(f"\nTime of leaning last: {datetime.datetime.now() - start}, for {GENERATIONS} generations.")
    print(f"Best score was: {best_score} and best time was {best_time}.")
    print(f"Age: {generation} generations.")

    if save:
        with open(MODEL_PATH, "wb") as f:
            data = (q_table, generation)
            pickle.dump(data, f)
    if GATHER_DATA:
        with open(DATA_PATH, "wb") as f:
            pickle.dump(gameplay_data, f)


if __name__ == "__main__":
    main(VISUAL)
