import numpy
from PIL import Image

def create_image(width = 1920, height = 1080 , name = 'random.png'):
    imarray = numpy.random.rand(width,height,3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    im.save(name)

def create_n_images(width=400 , height = 400, num = 100):
    for n in range(num):
        create_image(width, height, ('random'+str(n+1)+'.png'))

def create_image_with_color_prop(width = 64, height = 64, prop_red = 33, prop_green = 34, prop_blue = 33):
  return create_img_from_bytearray(create_bytearray_with_color_prop(width, height, prop_red, prop_green, prop_blue), 'RGBA')

def create_bytearray_with_color_prop(width = 64, height = 64, prop_red = 33, prop_green = 34, prop_blue = 33):
    #Initalize array with zeros
    imarray = numpy.random.rand(width * height, 3) * 0
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
    
    numpy.random.shuffle(imarray)
    immatrix = numpy.random.rand(height, width, 3) * 0
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