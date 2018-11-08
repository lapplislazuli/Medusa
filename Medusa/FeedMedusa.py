import pymongo 
from PIL import Image
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
# Helper libraries
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io


def load_model(path):
    loaded = tf.keras.models.load_model(
        path,
        custom_objects=None,
        compile=True
    )
    return loaded

def create_bytearray_with_color_prop(width = 64, height = 64, prop_red = 33, prop_green = 33, prop_blue = 33):
    #Initalize array with zeros
    imarray = numpy.random.rand(width * height, 3) * 0
    red_pixel = prop_red/100*width*height
    green_pixel = prop_green/100*width*height
    blue_pixel = prop_blue/100*width*height
    for x in range(height):
        for y in range(width):
            if(red_pixel > 0):
                imarray[x*width+y] = [255,0,0]
                red_pixel-= 1
            elif(green_pixel > 0):
                imarray[x*width+y] = [0,255,0]
                green_pixel-= 1
            elif(blue_pixel > 0):
                imarray[x*width+y] = [0,0,255]
                blue_pixel-= 1
            else:
                #Wrong proportion --> white pixel
                imarray[x*width+y] = [255,255,255]
    
    numpy.random.shuffle(imarray)
    immatrix = numpy.random.rand(height, width, 3) * 0
    for x in range(height):
        for y in range(width):
            immatrix[x,y] = imarray[x*width+y]
    casted = immatrix.astype('uint8')
    return casted


def create_img_from_bytearray(bytearr, colorscheme='RGBA'):
    im=Image.fromarray(bytearr).convert(colorscheme)
    return im

def create_and_rate_image(model):
    i = create_bytearray_with_color_prop()
    img = (numpy.expand_dims(i,0))
    return model.predict(img)