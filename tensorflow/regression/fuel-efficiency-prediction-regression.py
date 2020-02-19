"""
A simple program to predict fuel efficiency using regression methods
"""
# reference: https://www.tensorflow.org/tutorials


from __future__ import absolute_import, division, print_function, unicode_literals

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print("----------------------------------")
print("Tensorflow version: ", tf.__version__)
print("----------------------------------")

print("Downloading Auto MPG dataset")
dataset_path = keras.utils.get_file("auto-mpg.data",
                                    "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
print("Dataset Path: ", dataset_path)
print("----------------------------------")
print("Import dataset using Pandas")
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight',
                'Acceleration', 'Model Year', 'Origin']
raw_dataset = pd.read_csv(dataset_path, names=column_names,
                          na_values="?", comment='\t',
                          sep=" ", skipinitialspace=True)

dataset = raw_dataset.copy()
print("dataset.tail(): ")
print(dataset.tail())

print("Clean the data:")
print(dataset.isna().sum())

print("To keep this initial tutorial simple drop those rows.")
dataset = dataset.dropna()

print("The Origin column is really categorical, not numeric. So convert that to a one-hot:")
origin = dataset.pop('Origin')

dataset['USA'] = (origin == 1) * 1.0
dataset['Europe'] = (origin == 2) * 1.0
dataset['Japan'] = (origin == 3) * 1.0
print(dataset.tail())
print("----------------------------------")
print("Split the data into train and test")
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)
print("----------------------------------")
print("Inspect the data")
sns.pairplot(train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")
plt.show()

train_stats = train_dataset.describe()
train_stats.pop("MPG")
train_stats = train_stats.transpose()

print("train_stats")
print(train_stats)
print("----------------------------------")
print("Splitting features from labels")
train_labels = train_dataset.pop('MPG')
test_labels = test_dataset.pop('MPG')


def norm(x):
    return (x - train_stats['mean']) / train_stats['std']


print("----------------------------------")
print("Normalizing the data")
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)


def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model


print("----------------------------------")
print("Building the model")
model = build_model()
print("----------------------------------")
print("Inspecting the model")
model.summary()
print("----------------------------------")
print("Trying out the model by taking a batch of 10 examples")
example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
print("Example result: ")
print(example_result)


# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')


EPOCHS = 1000
print("----------------------------------")
print("Training the model")
history = model.fit(
    normed_train_data, train_labels,
    epochs=EPOCHS, validation_split=0.2, verbose=0,
    callbacks=[PrintDot()])

print("----------------------------------")
print("Visualizing the model")

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()


def plot_history(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mae'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mae'],
             label='Val Error')
    plt.ylim([0, 5])
    plt.legend()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mse'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mse'],
             label='Val Error')
    plt.ylim([0, 20])
    plt.legend()
    plt.show()


print("----------------------------------")
print("Plotting")
plot_history(history)

print("----------------------------------")
print("Building model")
model = build_model()

# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                    validation_split=0.2, verbose=0, callbacks=[early_stop, PrintDot()])

print("----------------------------------")
print("Plotting")
plot_history(history)

print("----------------------------------")
print("Evaluating model")
loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)

print("----------------------------------")
print("Testing set Mean Abs Error: {:5.2f} MPG".format(mae))

print("----------------------------------")
print("Making predictions")
test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [MPG]')
plt.ylabel('Predictions [MPG]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

error = test_predictions - test_labels
plt.hist(error, bins=25)
plt.xlabel("Prediction Error [MPG]")
_ = plt.ylabel("Count")

print("----------------------------------")
print("Program completed")
print("----------------------------------")
