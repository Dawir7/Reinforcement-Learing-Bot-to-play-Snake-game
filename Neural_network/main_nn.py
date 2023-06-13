import pygame
import numpy as np
import pickle
import datetime
import os
from snake import Snake
from map import Map
from agent import Agent
from keras.models import load_model

# Version 1.1
MODEL_DIR = "neural_models"
MODEL_NAME = "model_1v7_2"  # Name of the pickle file in which we store our model.
MODEL_PATH = os.path.join(MODEL_DIR, f"{MODEL_NAME}.h5")
# MODEL_NAME = "models/Best_model"  # Name of the pickle file in which we store our model.

GATHER_DATA = True
DATA_DIR = "../data"
DATA_PATH = os.path.join(DATA_DIR, f"data_{MODEL_NAME}")

learn = 0
if learn:
    VISUAL = False
    GENERATIONS = 900
    save = False

else:
    VISUAL = True
    GENERATIONS = 30
    save = False


MAX_ITERATIONS = 7_000
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
    model = load_model(MODEL_PATH)

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
        current_state = agent.get_state(snake, playground)

        snake.reset()
        playground.reset()

        if visual:
            pygame.display.set_caption(f"Snake Game, Neural Model")

        for iteration in range(MAX_ITERATIONS):

            if visual:
                clock.tick(30)
                pygame.time.delay(20)
                redraw_window(win, snake, playground)

            prediction = model.predict([current_state], verbose=None)
            # print(prediction, np.argmax(prediction))
            action = np.argmax(prediction)

            snake.move_action(action, visual)
            playground.random_snack_pos(snake)

            next_state = agent.get_state(snake, playground)
            game_over, reward = snake.collision(playground, add_snack=True)

            if game_over:
                if playground.score > best_score:
                    best_score = playground.score
                if iteration > best_time:
                    best_time = iteration
                break

            if visual:
                print(f"SCORE: {playground.score}")
                # print(f"Reward: {reward}, time: {iteration} iterations")

            current_state = next_state

        generation_time.append(iteration)


    print(f"\nTime of leaning last: {datetime.datetime.now() - start}, for {GENERATIONS} generations.")
    print(f"Best score was: {best_score} and best time was {best_time}.")


if __name__ == "__main__":
    main(VISUAL)
