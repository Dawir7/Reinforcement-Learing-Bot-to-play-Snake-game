from keras import layers, models, Input, losses
import os
import pickle
import numpy as np


MODEL_NAME = "model_1v7_2"
DATA_DIR = r'..\data'
MODEL_DIR = "neural_models"

DATA_PATH = os.path.join(DATA_DIR, f"data_{MODEL_NAME}")
MODEL_PATH = os.path.join(MODEL_DIR, f"{MODEL_NAME}.h5")
SHAPE = (None, 11)

TRAIN_DATA_SIZE = 0.8
EPOCHS = 5
BATCH = 200


def built_model(data_train, labels_train, data_val, labels_val):
    model = models.Sequential()
    model.add(Input(shape=SHAPE))
    # model.add(layers.Dense(5, input_shape=(5), activation='relu'))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(3, activation='softmax'))

    model.compile(optimizer='adam', loss=losses.SparseCategoricalCrossentropy(), metrics=["accuracy"])
    print("Start to learn model...")
    model.fit(data_train, labels_train, epochs=EPOCHS, batch_size=BATCH, validation_data=(data_val, labels_val))
    print("Model learned")
    return model


def main():
    if os.path.isfile(DATA_PATH):
        with open(DATA_PATH, 'rb') as f:
            gameplay_data = pickle.load(f)
    else:
        raise FileNotFoundError("Data file don't exist.")

    if not os.path.isdir(MODEL_DIR):
        os.mkdir(MODEL_DIR)

    print("Splitting data")
    # train_data, validation_data = split_dataset(gameplay_data, left_size=0.7)
    data_train = []
    labels_train = []
    data_val = []
    labels_val = []
    data_size = len(gameplay_data)
    for index, data in enumerate(gameplay_data):
        if index / data_size <= TRAIN_DATA_SIZE:
            data_train.append(data[0])
            labels_train.append(data[1])
        else:
            data_val.append(data[0])
            labels_val.append(data[1])
    print("Data Split")
    print(np.array(data_train).shape, np.array(data_val).shape)
    model = built_model(np.array(data_train), np.array(labels_train), np.array(data_val), np.array(labels_val))

    model.save(MODEL_PATH)


if __name__ == "__main__":
    main()
