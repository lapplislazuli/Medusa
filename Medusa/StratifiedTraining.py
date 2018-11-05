# For Stratified Training
# Only Medium and Weak Examples as Binary Classification
# 50:50 Split
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
# Also Requires pyyaml and h5py installed with pip

def train_model(trainingsize=12000,epochs=5):
    cursor = get_Image_cursor(getMedusaTrainingCollection())
    print("Creating Model...")
    model=create_model()
    print("Loading Images...")
    images,labels = prepare_data_for_tf(cursor,trainingsize)
    labels=np.asarray(labels,dtype=bool)
    print("Train Model")
    history = model.fit(images,labels,epochs=epochs)
    plot_history(history,epochs)
    return model

def test_model(model, testSize=2000):
    cursor = get_Image_cursor(getMedusaTestCollection())
    images,labels = prepare_data_for_tf(cursor,testSize)
    labels=np.asarray(labels,dtype=bool)
    test_loss, test_acc = model.evaluate(images,labels)
    print('Test accuracy:', test_acc , " Test loss:" , test_loss)

def plot_history(history,epochs):
    epochsPlt = range(1, epochs + 1)
    plt.plot(epochsPlt, history.history['loss'], 'g', label='Training loss')
    plt.plot(epochsPlt, history.history['acc'], 'b', label='Training Accuracy')
    plt.title('Training Loss and Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('%')
    plt.legend()
    plt.show()
   
################# SetUp ###############################
uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"
label2num = {"weak":0,"medium":1} 
num2label = {0:"weak", 1:"medium"}

def create_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(64,64,3)), # We got 64x64x3 Values per Image 
        keras.layers.Dense(512, activation=tf.nn.relu),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(512, activation=tf.nn.relu),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(512, activation=tf.nn.tanh),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(256, activation=tf.nn.tanh),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(2, activation=tf.nn.sigmoid) #Binary: Weak or Medium
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(), 
                loss='binary_crossentropy',
                metrics=['accuracy'])
    return model


def label_to_int(label):
    if(label2num[label]):
        return label2num[label]
    
def int_to_label(number):
    if(num2label[number]):
        return num2label[number]

def prepare_data_for_tf(cursor, n):
    data = get_next_n_samples(cursor,n)
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
################# Mongo Helpers #######################
def getMedusaTrainingCollection():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    TrainingCollection = medusaDB["StratifiedTraining"]
    return TrainingCollection

def getMedusaTestCollection():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    TestCollection = medusaDB["StratifiedTest"]
    return TestCollection

def get_Image_cursor(collection):
    cursor = collection.find()
    return cursor

def get_next_n_samples(cursor,n = 100):
    samples = []
    for _ in range(n):
        entry = cursor.next()
        samples.append((entry["success"],entry["image"]))
    return samples
################# Save and Load #######################
def save_model(model, name):
        if(model and name):
                model.save(name)

def load_model(path):
        return keras.models.load_model(path)

################## Image Alternation ####################

def img_to_bytearray(Image):
    imgByteArr = io.BytesIO()
    Image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def create_img_from_mongoDBBytes(mongobytes, colorscheme='RGBA'):
    image = Image.open(io.BytesIO(mongobytes))
    return image
