import numpy
from PIL import Image

def create_image(width = 1920, height = 1080 , name = 'random.png'):
    imarray = numpy.random.rand(width,height,3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    im.save(name)

def create_n_images(width=400 , height = 400, num = 100):
    for n in range(num):
        create_image(width, height, ('random'+str(n+1)+'.png'))