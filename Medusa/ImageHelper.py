import numpy as np
from PIL import Image, ImageEnhance
import io

# Makes int -> float in image, labels to ints, and lists to arrays
def prepareTrafficSigns(images,labels):
    rimages = np.asarray(images)
    rlabels = np.asarray(labels,dtype=int)
    rimages = rimages/255 # Change to float
    return rimages,rlabels

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