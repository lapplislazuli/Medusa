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
import matplotlib.image as mpimg
import io

uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"
label2num = {"weak":1,"medium":2,"strong":3} 
num2label = {1:"weak", 2:"medium", 3:"strong"}

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
        keras.layers.Dense(4, activation=tf.nn.softmax) #3 Classes: Weak, Medium, Strong
    ])
    model.compile(optimizer=tf.train.AdamOptimizer(), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return model


def img_to_bytearray(Image):
    imgByteArr = io.BytesIO()
    Image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def create_img_from_mongoDBBytes(mongobytes, colorscheme='RGBA'):
    image = Image.open(io.BytesIO(mongobytes))
    return image

def label_to_int(label):
    if(label2num[label]):
        return label2num[label]
    
def int_to_label(number):
    if(num2label[number]):
        return num2label[number]
    
def train_model(batchsize=100):
    cursor = get_Image_cursor()
    model=create_model()
    data = get_next_n_samples(cursor,batchsize)
    images = []
    labels = []
    for i in range(batchsize):
        images.append(mpimg.pil_to_array(create_img_from_mongoDBBytes(data[i][1])))
        labels.append(label_to_int(data[i][0]))
    #List 2 Array
    images = np.asarray(images)
    #Removing AlphaValues (They're always 255)
    images = images[:,:,:,0:3]
    labels = np.asarray(labels)
    model.fit(images,labels,epochs=5)
