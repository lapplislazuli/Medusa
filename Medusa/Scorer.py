import requests
import json
import time

import numpy as np
import matplotlib.image as mpimg

import MedusaMongo as MMongo
import ImageGenerator as MImg
import ImageHelper as ImgHelper
# Variables required through the process

url = 'https://phinau.de/trasi'
access_key = 'ehiefoveingereim3ooD2vo8reeb9ooz'
credentials = {'key': access_key}

# Request functionality
def send_img_bytearray(nipples):
    file_to_upload = {'image': nipples}
    post_request = requests.post(url, files=file_to_upload, data=credentials)
    return post_request

def response_scores_toJSON(post_request):
    if post_request.text:
        return json.loads(post_request.text)

def get_trasi_score(image):
    img_bytes = ImgHelper.img_to_bytearray(image)
    response = send_img_bytearray(img_bytes)
    if(response.status_code==200):
        return response_scores_toJSON(response)
    else:
        print('Error - HTTPStatusCode', response.status_code)

def get_best_score(ResponseText):
    scores = json.loads(ResponseText)
    return scores[0].get('confidence')

def send_ppm_image(img):
    parsedImg = ImgHelper.create_img_from_bytearray(img)
    img_bytes = ImgHelper.img_to_bytearray(parsedImg)
    response = send_img_bytearray(img_bytes)
    return response

def get_img_trasi_score_tuple(image):
        return image, get_trasi_score(image)

def get_img_trasi_aphrodite_score_triple(image, model):
        image_array = mpimg.pil_to_array(image)
        image_array = np.asarray(image_array)
        image_array = image_array[:,:,0:3]
        image_array = image_array/255
        image_array = np.expand_dims(image_array,0)
        aphrodite_score = model.predict(image_array)
        return image, get_trasi_score(image), aphrodite_score