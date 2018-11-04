import numpy
from PIL import Image
import io
import requests
import json
import time
import pymongo
import datetime
import MedusaMongo as MMongo
# Variables required through the process

url = 'https://phinau.de/trasi'
access_key = 'ehiefoveingereim3ooD2vo8reeb9ooz'
credentials = {'key': access_key}

#Init the needed functions for images
def create_and_save_image(width = 64, height = 64 , name = 'random.png'):
    imarray = numpy.random.rand(width,height,3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    im.save(name)

def create_and_save_n_images(width=64 , height = 64, num = 100):
    for n in range(num):
        create_and_save_image(width, height, ('random'+str(n+1)+'.png'))
        
def create_bytearray(width=64,height=64):
    imarray = numpy.random.rand(width,height,3)*255
    casted = imarray.astype('uint8')
    return casted

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

def img_to_bytearray(Image):
    imgByteArr = io.BytesIO()
    Image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

# Request functionality
def send_img_bytearray(nipples):
    file_to_upload = {'image': nipples}
    post_request = requests.post(url, files=file_to_upload, data=credentials)
    return post_request

def response_scores_toJSON(post_request):
    if post_request.text:
        return json.loads(post_request.text)

# Full Logic

def full_loop():
    img_bytes = img_to_bytearray(create_img_from_bytearray(create_bytearray()))
    response = send_img_bytearray(img_bytes)
    if(response.status_code==200):
        MMongo.save_results_to_Mongo(response_scores_toJSON(response),img_bytes)
    else:
        print('Error - HTTPStatusCode', response.status_code)

def execute_timed_full_loops(MaxLoops,Intervall):
    print("Starting Scorer Loop")
    i=0
    while(i < MaxLoops):
        full_loop()
        time.sleep(Intervall)
        i+=1
        if(i%100 == 0):
            print("loop #"+str(i) + " done")
    print("Done")
