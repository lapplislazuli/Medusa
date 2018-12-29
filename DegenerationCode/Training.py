# To Train and Test an AI using the German Traffic Sign Recognition "Benchmark"-Dataset

# Requires the German Traffic Sign Recogintion Benchmark somewhere around you can point a path to
# can be found under http://benchmark.ini.rub.de/?section=gtsdb&subsection=dataset 
# but is annoyingly strong wrapped.
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np
import csv

import ImageHelper as ImgHelper

# For Image interpolation
from scipy import ndimage
from scipy import misc as scipyMisc
# For NNs
import tensorflow as tf
from tensorflow import keras

# Not used, just to show general flow how to train a model using this functions
# For the later Algorithms a model is required, not necessarily this one
def main(trainingdatapath, epochs=5,modelname="Aphrodite.h5"):
    rawI, rawL = readTrafficSignsBetter(trainingdatapath)
    goodI, goodL = ImgHelper.prepareTrafficSigns(rawI,rawL)
    model = create_conv2d_model()
    model.fit(goodI,goodL, epochs=epochs)
    save_model(model,modelname)

################ Data Prep ###################

## Mostly taken from the Python Example for the GTSRB for Loading
## But is much better, as I interpolate images to be 64x64
def readTrafficSignsBetter(rootpath):
    images = []
    labels = []
    for c in range(0,43):
        prefix = rootpath + '/' + format(c, '05d') + '/' # subdirectory for class
        gtFile = open(prefix + 'GT-'+ format(c, '05d') + '.csv') # annotations file
        gtReader = csv.reader(gtFile, delimiter=';') # csv parser for annotations file
        next(gtReader)
        # loop over all images in current annotations file
        for row in gtReader:
            i = mpimg.imread(prefix + row[0])
            a = scipyMisc.imresize(i, (64,64,3), interp='bilinear', mode=None)
            images.append(a) # the 1th column is the filename
            labels.append(row[7]) # the 8th column is the label
            #TODO: What are the other 6 columns?
        gtFile.close()
    return images, labels

######### Model Creation #####################
def create_conv2d_model():
    # Takes very long! 
    model = tf.keras.Sequential()
    model.add(keras.layers.Conv2D(32, (3, 3), padding='same',
                     input_shape=(64,64,3),
                     activation='relu'))
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Conv2D(64, (3, 3), padding='same',
                     activation='relu'))
    model.add(keras.layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dense(43, activation='softmax')) # we got 42 signs + 1 error
    
    model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
    return model

def create_simple_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(64,64,3)), # We got 64x64x3 Values per Image 
        keras.layers.Dense(100,activation=tf.nn.tanh),
        keras.layers.Dense(100,activation=tf.nn.leaky_relu),
        keras.layers.Dense(43, activation=tf.nn.softmax) 
    ])
    model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
    return model

####### Model Helpers #############
def plot_history(history,epochs):
    epochsPlt = range(1, epochs + 1)
    plt.plot(epochsPlt, history.history['loss'], 'g', label='Training loss')
    plt.plot(epochsPlt, history.history['acc'], 'b', label='Training Accuracy')
    plt.title('Training Loss and Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('%')
    plt.legend()
    plt.show()

def save_model(model, name):
        if(model and name):
                model.save(name)

def load_model(path):
    loaded = tf.keras.models.load_model(
        path,
        custom_objects=None,
        compile=False
    )
    loaded.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
    return loaded