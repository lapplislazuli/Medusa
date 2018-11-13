## This tricks our AI
## Requires real-images and our AI somewhere around to point with path

import numpy as np

import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# IMG MANIPULATION
from scipy import ndimage
from scipy import misc as scipyMisc
from PIL import Image

import FeedAphrodite as FA
import AphroditeTraining as AT
import ImageGenerator as MImg

def main():
    StoppschildLabel=10 #I dont know, its just to Show
    img = load_ppm_image("Stoppschilder/Example")
    model = AT.load_model("Aphrodite.h5")
    _, degImage = degenerate(model,img,StoppschildLabel,iterations=100)
    DImg= MImg.create_img_from_bytearray(degImage)
    DImg.save("Stoppschilder/DegExample")

def degenerate(model, image, label, decay = 0.01, iterations = 10):
    totalLoops = 0
    oldScores,oldImage = predict_single_image(model,image)
    oldLabelScore=oldScores[label]
    it = 0 #Counts successfull loops!
    while(it<iterations):
        totalLoops+=1
        print("Depth:",it, "Loops:" , totalLoops)
        noise = _generate_noise(0.5)
        degenerated = oldImage.copy()+noise
        degenerated = np.asarray(degenerated,dtype="uint8")
        degScores,degImage = predict_single_image(model,degenerated)
        degLabelScore=degScores[label]
        if(degLabelScore> oldLabelScore-decay):
            oldImage=degImage
            oldLabelScore=degLabelScore
            it+=1
    return oldLabelScore,oldImage

def load_ppm_image(path):
    i = mpimg.imread(path)
    a = scipyMisc.imresize(i, (64,64,3), interp='bicubic', mode=None)
    return a

def _generate_noise(density,strength=10,width=64,height=64):
    noise = np.random.rand(width,height,3)
    noise -=0.5 # to run from [-0.5,0.5]
    noise*=strength
    noise = np.asarray(noise,dtype="int")
    return noise
    
def predict_single_image(model,img):
    imgArr = (np.expand_dims(img,0))
    return model.predict(imgArr)[0],img

