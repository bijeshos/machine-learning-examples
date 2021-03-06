"""
This is a sample program to perform image classification using Fashion MNIST image data set
"""
# reference: https://www.tensorflow.org/tutorials


from __future__ import absolute_import, division, print_function, unicode_literals

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import datetime

print("----------------------------------")
print("Tensorflow version: ", tf.__version__)
print("----------------------------------")

print("Importing MNIST dataset (using TFDS)")
train_tfds_dataset, test_tfds_dataset = tfds.load('mnist:3.*.*', split=['train', 'test'], batch_size=-1)

# convert to numpy array
train_dataset = tfds.as_numpy(train_tfds_dataset)
test_dataset = tfds.as_numpy(test_tfds_dataset)

# retrieve image and label arrays
train_images, train_labels = train_dataset["image"], train_dataset["label"]
test_images, test_labels = test_dataset["image"], test_dataset["label"]

# reshape current 4d array to 3d array
train_images = train_images.reshape(train_images.shape[0], train_images.shape[1], train_images.shape[2])
test_images = test_images.reshape(test_images.shape[0], test_images.shape[1], test_images.shape[2])

print("Storing class names")
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

class_names = ['Zero', 'One', 'Two', 'Three', 'Four',
               'Five', 'Six', 'Seven', 'Eight', 'Nine']

print("----------------------------------")
print("Exploring data")
print("Training image shape/format: ", train_images.shape)
print("Training labels shape/format: ", train_labels.shape)
print("Test image shape/format: ", test_images.shape)
print("Test labels shape/format: ", test_labels.shape)

print("Pre-processing data for display. Close popup to continue ...")
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

print("Scaling values")
train_images = train_images / 255.0
test_images = test_images / 255.0

print("Displaying first 25 images for verification. Close popup to continue ...")
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

print("----------------------------------")
print("Building the model")

print("Setting up the layers")
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

print("Compiling the model")
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# specify configuration for tensorboard
log_dir = "./../../logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

print("Training the model")
# use below line if tensorboard integration is not needed
# model.fit(train_images, train_labels, epochs=5)

history = model.fit(train_images,
          train_labels,
          epochs=5,
          validation_data=(test_images, test_labels),
          callbacks=[tensorboard_callback])

# get training parameters
history_dict = history.history
history_dict.keys()
train_accuracy = history_dict['accuracy']
train_val_accuracy = history_dict['val_accuracy']
train_loss = history_dict['loss']
train_val_loss = history_dict['val_loss']

print("Train : accuracy:", train_accuracy)
print("Train : val_accuracy:", train_val_accuracy)
print("Train : loss:", train_loss)
print("Train : val_loss:", train_val_loss)

print("Evaluating accuracy")
test_loss, test_accuracy = model.evaluate(test_images, test_labels)

print("Test loss:", test_loss)
print("Test accuracy:", test_accuracy)


print("----------------------------------")
print("Making predictions")
predictions = model.predict(test_images)

print("Prediction 0: ", predictions[0])

print("----------------------------------")
print("Label with highest confidence: ", np.argmax(predictions[0]))

print("Test Label 0: ", test_labels[0])
print("----------------------------------")
print("Plotting as a graph. Close popup to continue ...")


def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


print("Showing 0th image. Close popup to continue ...")
i = 0
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions, test_labels)
plt.show()

i = 12
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions, test_labels)
plt.show()

print("----------------------------------")
print("Plotting the first X test images, their predicted labels, and the true labels.")
print("Coloring correct predictions in blue and incorrect predictions in red.")
print("Close popup to continue ...")
num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions, test_labels, test_images)
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
    plot_value_array(i, predictions, test_labels)
plt.show()

print("----------------------------------")
print("Using trained model to make prediction")

print("Grabbing an image from the test dataset")
img = test_images[0]

print("Test image shape: ", img.shape)

print("Adding the image to a batch where it's the only member.")
img = (np.expand_dims(img, 0))

print("Test image shape: ", img.shape)

print("----------------------------------")
print("Predicting correct label for the image")
predictions_single = model.predict(img)
print("Single Prediction: ", predictions_single)

plot_value_array(0, predictions_single, test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)

np.argmax(predictions_single[0])

# todo: check this later
# file_writer = tf.summary.FileWriter('/path/to/logs', sess.graph)

print("----------------------------------")
print("Open a terminal in this dir and execute the following to view run details on tensorboard")
print("tensorboard --logdir ./../../logs/fit/")
print("----------------------------------")


print("----------------------------------")
print("Program completed")
print("----------------------------------")
