import numpy as np

import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# IMG MANIPULATION
from scipy import ndimage
from scipy import misc as scipyMisc

import MedusaMongo as MMongo
import ImageGenerator as MImg

from PIL import Image
import requests
import json
import time

url = 'https://phinau.de/trasi'
access_key = 'ehiefoveingereim3ooD2vo8reeb9ooz'
credentials = {'key': access_key}

def remoteDegenerate(image, decay = 0.01, iterations = 10):
    initialResp = _send_ppm_image(img)
    if(initialResp.status_code!=200):
        return
    totalLoops = 0
    lastImg = img
    lastScore = __get_best_score(initialResp.text)
    
    print("StartConfidence:",lastScore)
    it = 0 #Counts successfull loops!
    while(it<iterations and totalLoops<2000):
        totalLoops+=1
        degenerated = alterImage(lastImg.copy(),7)
        degeneratedResp = _send_ppm_image(degenerated)
        degeneratedScore=__get_best_score(degeneratedResp.text)
        print("Score:",degeneratedScore,"Depth:",it, "Loop:" , totalLoops)
        if(degeneratedScore> lastScore-decay):
            lastImg=degenerated
            lastScore=degeneratedScore
            it+=1
        time.sleep(1.1)
    return lastScore,lastImg

def create_img_from_bytearray(bytearr, colorscheme='RGB'):
    im=Image.fromarray(bytearr, colorscheme)
    return im

def send_img_bytearray(nipples):
    file_to_upload = {'image': nipples}
    post_request = requests.post(url, files=file_to_upload, data=credentials)
    return post_request

def __response_scores_toJSON(post_request):
    if post_request.text:
        return json.loads(post_request.text)

        def load_ppm_image(path):
    i = mpimg.imread(path)
    a = scipyMisc.imresize(i, (64,64,3), interp='bicubic', mode=None)
    return a

def _generate_noise(density,strength=10,width=64,height=64):
    noise = np.random.rand(width,height,3)
    noise -=0.5 # to run from [-0.5,0.5]
    noise*=strength
    noise = np.asarray(noise,dtype="int")
    return noise
    
def _alterImage(image,strength=8):
    noise = _generate_noise(0.5,strength)
    degenerated = image+noise
    degenerated = np.asarray(degenerated,dtype="uint8")
    return degenerated

def __get_best_score(ResponseText):
    scores = json.loads(ResponseText)
    return scores[0].get('confidence')

def _send_ppm_image(img):
    parsedImg = create_img_from_bytearray(img)
    img_bytes = MImg.img_to_bytearray(parsedImg)
    response = send_img_bytearray(img_bytes)
    return response