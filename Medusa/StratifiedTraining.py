# For Stratified Training
# Only Medium and Weak Examples as Binary Classification
# 50:50 Split
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
    
def train_model(trainingsize=12000):
    cursor = MMongo.get_Image_cursor(MMongo.getMedusaTrainingCollection())
    model=create_model()
    images,labels = prepare_data_for_tf(cursor,trainingsize)
    labels=np.asarray(labels,dtype=bool)
    model.fit(images,labels,epochs=5)
    return model

def test_model(model, testSize=2000):
    cursor = MMongo.get_Image_cursor(MMongo.getMedusaTestCollection())
    images,labels = prepare_data_for_tf(cursor,testSize)
    labels=np.asarray(labels,dtype=bool)
    test_loss, test_acc = model.evaluate(images,labels)
    print('Test accuracy:', test_acc)

################# SetUp ###############################
label2num = {"weak":0,"medium":1} 
num2label = {0:"weak", 1:"medium"}

def create_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(64,64,3)), # We got 64x64x3 Values per Image 
        keras.layers.Dense(512, activation=tf.nn.leaky_relu),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(512, activation=tf.nn.relu),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(512, activation=tf.nn.tanh),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(256, activation=tf.nn.tanh),
        keras.layers.Dense(128, activation=tf.nn.leaky_relu),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(2, activation=tf.nn.sigmoid) #Binary: Weak or Medium
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(), 
                loss=tf.losses.sigmoid_cross_entropy,
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
