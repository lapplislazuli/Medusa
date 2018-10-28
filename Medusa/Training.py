# This is for Medusa Training
# it includes setting up Tensorflow
# Curling MongoDB
# Storing Model
import pymongo 
from PIL import Image
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"
cursor = pymongo.cursor

def getMedusaImageCollection():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    imageCollection = medusaDB["Images"]
    return imageCollection

def get_Image_cursor():
    imageCollection = getMedusaImageCollection()
    cursor = imageCollection.find()
    return cursor

def get_next_n_samples(cursor,n = 100):
    samples = []
    for _ in range(n):
        entry = cursor.next()
        samples.append((entry["success"],entry["image"]))
    return samples

def create_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(64,64,3)), # We got 64x64x3 Values per Image 
        keras.layers.Dense(128, activation=tf.nn.relu), 
        keras.layers.Dense(3, activation=tf.nn.softmax) #3 Classes: Weak, Medium, Strong
    ])
    model.compile(optimizer=tf.train.AdamOptimizer(), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return model

def train_model(batchsize=100):
    model=create_model()
    data = get_next_n_samples(batchsize)
    images = []
    labels = []
    for i in range(batchsize):
        images.append(data[i][2])
        labels.append(data[i][1])
    model.fit(images,labels,epochs=5)