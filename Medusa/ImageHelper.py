import numpy as np
from PIL import Image, ImageEnhance
import io

import matplotlib.image as mpimg

from scipy import ndimage
from scipy import misc as scipyMisc

# Makes int -> float in image, labels to ints, and lists to arrays
def prepareTrafficSigns(images,labels):
    rimages = np.asarray(images)
    rlabels = np.asarray(labels,dtype=int)
    rimages = rimages/255 # Change to float
    return rimages,rlabels

# Loads an ppm image as bytearray from a path and resizes it to our required shape (64,64,3) 
# The bicubic interpolation looks "best" imo, others are 'nearest' and 'bilinear'
# Used for AphroditeTraining and in Degeneration 
def load_ppm_image(path, interpolation = 'bicubic'):
    raw = mpimg.imread(path)
    return scipyMisc.imresize(raw, (64,64,3), interp=interpolation, mode=None)

################## Image Alternation ####################
# Creates the required bytearray for trasi webinterface
# Sadly it doesnt take our nice numpy bytearrays, but requires a binary saved png
# Therefore we store it to an in memory stream as byte, and read the in memory stream
def img_to_bytearray(Image):
    imgByteArr = io.BytesIO()
    Image.save(imgByteArr, format='PNG')
    return imgByteArr.getvalue()

# Takes the image blob from MongoDB and parses it to a PIL Img
def create_img_from_mongoDBBytes(mongobytes, colorscheme='RGBA'):
    return Image.open(io.BytesIO(mongobytes))

# Takes and uint Rgb bytearray and outputs PIL Image
def create_img_from_bytearray(bytearr, colorscheme='RGBA'):
    return Image.fromarray(bytearr).convert(colorscheme)

def change_brigthness_of_img(image, brightnessFactor=1.0):
    changedImage = ImageEnhance.Brightness(image).enhance(brightnessFactor)
    return changedImage

def change_contrast_of_img(image, contrastFactor=1.0):
    changedImage = ImageEnhance.Contrast(image).enhance(contrastFactor)
    return changedImage