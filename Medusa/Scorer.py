import requests
import json
import time

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
