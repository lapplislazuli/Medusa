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

def __propFilter(value,prop):
    return value if(numpy.random.rand()<prop) else 0

def create_image_with_color_prop(width = 64, height = 64, prop_red = 33, prop_green = 34, prop_blue = 33):
  return create_img_from_bytearray(create_bytearray_with_color_prop(width, height, prop_red, prop_green, prop_blue), 'RGBA')

def _create_red_image_part(prop):
    imarray = numpy.asarray([(propFilter(redpart,prop),0,0) for redpart in numpy.random.rand(64*64)*255])
    imarray.shape=(64,64,3)
    return imarray.astype('uint8')

def _create_green_image_part(prop):
    imarray = numpy.asarray([(0,propFilter(greenpart,prop),0) for greenpart in numpy.random.rand(64*64)*255])
    imarray.shape=(64,64,3)
    return imarray.astype('uint8')

def _create_blue_image_part(prop):
    imarray = numpy.asarray([(0,0,propFilter(bluepart,prop)) for bluepart in numpy.random.rand(64*64)*255])
    imarray.shape=(64,64,3)
    return imarray.astype('uint8')

def create_bytearray_with_color_prop(width = 64, height = 64, prop_red = 1, prop_green = 1, prop_blue = 1):
    return _create_red_image_part(prop_red)+_create_blue_image_part(prop_blue)+_create_green_image_part(prop_green)

def create_img_from_bytearray(bytearr, colorscheme='RGBA'):
    im=Image.fromarray(bytearr).convert(colorscheme)
    return im

#From Scorer
def create_bytearray(width=64,height=64):
    imarray = random.rand(width,height,3)*255
    casted = imarray.astype('uint8')
    return casted


