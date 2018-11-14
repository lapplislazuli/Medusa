import numpy as np
from PIL import Image, ImageEnhance
import io

import matplotlib.image as mpimg

# IMG MANIPULATION
from scipy import ndimage
from scipy import misc as scipyMisc

# Makes int -> float in image, labels to ints, and lists to arrays
def prepareTrafficSigns(images,labels):
    rimages = np.asarray(images)
    rlabels = np.asarray(labels,dtype=int)
    rimages = rimages/255 # Change to float
    return rimages,rlabels

def load_ppm_image(path):
    i = mpimg.imread(path)
    a = scipyMisc.imresize(i, (64,64,3), interp='bicubic', mode=None)
    return a

def change_brigthness_of_img(image, brightnessFactor=1.0):
    changedImage = ImageEnhance.Brightness(image).enhance(brightnessFactor)
    return changedImage

def change_contrast_of_img(image, contrastFactor=1.0):
    changedImage = ImageEnhance.Contrast(image).enhance(contrastFactor)
    return changedImage

################## Image Alternation ####################

def img_to_bytearray(Image):
    imgByteArr = io.BytesIO()
    Image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def create_img_from_mongoDBBytes(mongobytes, colorscheme='RGBA'):
    image = Image.open(io.BytesIO(mongobytes))
    return image

def create_img_from_bytearray(bytearr, colorscheme='RGBA'):
    im=Image.fromarray(bytearr).convert(colorscheme)
    return im