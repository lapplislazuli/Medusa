import numpy
from PIL import Image
import io
import requests
import json
import time
import pymongo
import datetime
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

# Saving to Mongo

#User: MedusaUser
#PW: P3R5EU? 
mongoURI = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"
mongoClient=pymongo.MongoClient(mongoURI)
medusaDB = mongoClient["Medusa"]
imageCollection = medusaDB["Images"]

def save_results_to_Mongo(scores,imgBytes):
    imageCollection.insert_one({
        "scores":scores,
        "insert_date":str(datetime.datetime.now()),
        "image":imgBytes
    }
    )

# Full Logic

def full_loop():
    img_bytes = img_to_bytearray(create_img_from_bytearray(create_bytearray()))
    response = send_img_bytearray(img_bytes)
    if(response.status_code==200):
        save_results_to_Mongo(response_scores_toJSON(response),img_bytes)
    else:
        #throw errors? Show me something?
        print('upsie')

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
