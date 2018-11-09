from numpy import random
import numpy

import io
from PIL import Image, ImageEnhance

def create_image(width = 64, height = 64):
    imarray = random.rand(width,height,3)
    return imarray

def create_n_images(n):
    batch = []
    for i in range(n):
        batch.append(create_image())
    return numpy.asarray(batch)

def create_image_with_color_prop(width = 64, height = 64, prop_red = 33, prop_green = 34, prop_blue = 33):
  return create_img_from_bytearray(create_bytearray_with_color_prop(width, height, prop_red, prop_green, prop_blue), 'RGBA')

def create_bytearray_with_color_prop(width = 64, height = 64, prop_red = 33, prop_green = 34, prop_blue = 33):
    #Initalize array with zeros
    imarray = random.rand(width * height, 3) * 0
    red_pixel = prop_red/100*width*height
    green_pixel = prop_green/100*width*height
    blue_pixel = prop_blue/100*width*height
    for x in range(height):
        for y in range(width):
            if(red_pixel > 0):
                imarray[x*width+y] = [random.random() * 255,0,0]
                red_pixel-= 1
            elif(green_pixel > 0):
                imarray[x*width+y] = [0,random.random() * 255,0]
                green_pixel-= 1
            elif(blue_pixel > 0):
                imarray[x*width+y] = [0,0,random.random() * 255]
                blue_pixel-= 1
            else:
                #Wrong proportion --> white pixel
                imarray[x*width+y] = [255,255,255]
    
    random.shuffle(imarray)
    immatrix = random.rand(height, width, 3) * 0
    for x in range(height):
        for y in range(width):
            immatrix[x,y] = imarray[x*width+y]
    casted = immatrix.astype('uint8')
    return casted

def change_brigthness_of_img(image, brightnessFactor=1.0):
    changedImage = ImageEnhance.Brightness(image).enhance(brightnessFactor)
    return changedImage

def change_contrast_of_img(image, contrastFactor=1.0):
    changedImage = ImageEnhance.Contrast(image).enhance(contrastFactor)
    return changedImage

def create_img_from_bytearray(bytearr, colorscheme='RGBA'):
    im=Image.fromarray(bytearr).convert(colorscheme)
    return im

#From Scorer
def create_bytearray(width=64,height=64):
    imarray = random.rand(width,height,3)*255
    casted = imarray.astype('uint8')
    return casted

def img_to_bytearray(Image):
    imgByteArr = io.BytesIO()
    Image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
