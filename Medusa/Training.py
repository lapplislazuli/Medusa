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

import MedusaMongo as MMongo
# Also Requires pyyaml and h5py installed with pip

    
def train_model(trainingsize=100):
    cursor = MMongo.get_Image_cursor(MMongo.getMedusaTrainingCollection())
    model=create_model()
    images,labels = prepare_data_for_tf(cursor,trainingsize)
    model.fit(images,labels,epochs=5)
    return model

def test_model(model, testSize=4000):
    cursor = MMongo.get_Image_cursor(MMongo.getMedusaTestCollection())
    images,labels = prepare_data_for_tf(cursor,testSize)
    test_loss, test_acc = model.evaluate(images,labels)
    print('Test accuracy:', test_acc)

################# SetUp ###############################
uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"
label2num = {"weak":1,"medium":2,"strong":3} 
num2label = {1:"weak", 2:"medium", 3:"strong"}

def create_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(64,64,3)), # We got 64x64x3 Values per Image 
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(256, activation=tf.nn.relu),
        keras.layers.Dense(4, activation=tf.nn.softmax) #3 Classes: Weak, Medium, Strong
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(), 
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['accuracy'])

    return model

def label_to_int(label):
    if(label2num[label]):
        return label2num[label]
    
def int_to_label(number):
    if(num2label[number]):
        return num2label[number]

def prepare_data_for_tf(cursor, n):
    data = MMongo.get_next_n_samples(cursor,n)
    images = []
    labels = []
    for i in range(n):
        images.append(mpimg.pil_to_array(create_img_from_mongoDBBytes(data[i][1])))
        labels.append(label_to_int(data[i][0]))
    #List 2 Array
    images = np.asarray(images)
    #Removing AlphaValues (They're always 255)
    images = images[:,:,:,0:3]
    #Norming RGB Values to 1
    images = images/255 
    labels = np.asarray(labels)
    return images,labels
################# Save and Load #######################
def save_model(model, name):
        if(model and name):
                model.save(name)

def load_model(path):
        keras.models.load_model(path)

################## Image Alternation ####################

def img_to_bytearray(Image):
    imgByteArr = io.BytesIO()
    Image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def create_img_from_mongoDBBytes(mongobytes, colorscheme='RGBA'):
    image = Image.open(io.BytesIO(mongobytes))
    return image
