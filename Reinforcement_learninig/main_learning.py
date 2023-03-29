import pygame
import numpy as np
import pickle
import datetime

from snake import Snake
from map import Map
from agent import Agent

# Version 0.8
MODEL_NAME = "models/model_0v8"  # Name of the pickle file in which we store our model.

VISUAL = False
GENERATIONS = 100_000
# VISUAL = True
# GENERATIONS = 30
MAX_ITERATIONS = 10_000  # max iterations in game
# epsilon = 1  # epsilon = 0.7 - generation * 0.01
MIN_EPSILON = 0.000_001
epsilon_dec = 0.000_01
GAMMA = 0.5
LEARNING_RATE = 0.75  # ATTENTION: From model 0v5 this is change dynamically.
MIN_LEARNING_RATE = 0.3


def redraw_window(win: pygame.display.set_mode, snake: Snake, playground: Map):
    win.fill((25, 119, 207))
    playground.draw(win)
    snake.draw(win, playground)
    pygame.display.update()  # This updates the screen so we can see our rectangle


def main(visual: bool = True):
    start = datetime.datetime.now()
    best_score = 0
    best_time = 0
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

            snake.move_action(action, visual)
            playground.random_snack_pos(snake)

            # It can be as one function.
            next_state = agent.get_state(snake, playground)
            next_binary_state = agent.make_binary(next_state)
            game_over, reward = snake.collision(playground, add_snack=True)

            bellman_equation = (1 - LEARNING_RATE) * q_table[int(current_binary_state, 2), action] + LEARNING_RATE *\
                               (reward + GAMMA * max(q_table[int(next_binary_state, 2), :]))
            q_table[int(current_binary_state, 2), action] = bellman_equation

            generation_reward += reward

            if game_over:
                # ToDo: Add some kind of a delay/freeze so we know new generation is coming.
                # print(f"\n\nGAME OVER, GENERATION {generation}, LAST: {iteration} Iterations")
                # print(f"Achieved Score: {playground.score}\n\n")
                if playground.score > best_score:
                    best_score = playground.score
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
        if generation % 10_000 == 0:
            print(generation, datetime.timedelta(milliseconds=int(np.sum(generation_time[-10_000:-1]))))

    print(f"\nTime of leaning last: {datetime.datetime.now() - start}, for {GENERATIONS} generations.")
    print(f"Best score was: {best_score} and best time was {best_time}.")
    print(f"Age: {generation} generations.")

    with open(f"{MODEL_NAME}", "wb") as f:
        data = (q_table, generation)
        pickle.dump(data, f)


if __name__ == "__main__":
    main(VISUAL)
