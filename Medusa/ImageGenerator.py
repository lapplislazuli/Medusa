import numpy
from numpy import random

import ImageHelper as ImgHelper

def create_image(width = 64, height = 64):
    return random.rand(width,height,3).astype('uint8')

def create_n_images(n):
    return numpy.asarray([create_image() for i in range(n)])

def create_image_with_color_prop(width = 64, height = 64, prop_red = 33, prop_green = 34, prop_blue = 33):
  return ImgHelper.create_img_from_bytearray(create_bytearray_with_color_prop(width, height, prop_red, prop_green, prop_blue), 'RGBA')

def create_bytearray_with_color_prop(redProp,blueProp,greenProp,width=64,heigth=64):
    redPart   = numpy.asarray([v if redProp>numpy.random.rand() else 0 for v in numpy.random.rand(width*heigth)*255]).reshape((width,heigth))
    bluePart  = numpy.asarray([v if blueProp>numpy.random.rand() else 0 for v in numpy.random.rand(width*heigth)*255]).reshape((width,heigth))
    greenPart = numpy.asarray([v if greenProp>numpy.random.rand() else 0 for v in numpy.random.rand(width*heigth)*255]).reshape((width,heigth))
    return numpy.asarray([redPart,bluePart,greenPart]).transpose(1,2,0).astype('uint8')