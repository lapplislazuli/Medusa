import numpy as np

import tensorflow as tf
from tensorflow import keras

import MedusaMongo as MMongo
import ImageGenerator as MImg

from PIL import Image
import time

import Scorer as Scorer
import ImageHelper as ImgHelper

url = 'https://phinau.de/trasi'
access_key = 'ehiefoveingereim3ooD2vo8reeb9ooz'
credentials = {'key': access_key}

def remoteDegenerate(image, decay = 0.01, iterations = 10):
    initialResp = Scorer.send_ppm_image(image)
    if(initialResp.status_code!=200):
        return
    totalLoops = 0
    lastImg = image
    lastScore = Scorer.get_best_score(initialResp.text)
    
    print("StartConfidence:",lastScore)
    it = 0 #Counts successfull loops!
    while(it<iterations and totalLoops<2000):
        totalLoops+=1
        degenerated = _alterImage(lastImg.copy(),7)
        degeneratedResp = Scorer.send_ppm_image(degenerated)
        degeneratedScore= Scorer.get_best_score(degeneratedResp.text)
        print("Score:",degeneratedScore,"Depth:",it, "Loop:" , totalLoops)
        if(degeneratedScore> lastScore-decay):
            lastImg=degenerated
            lastScore=degeneratedScore
            it+=1
        time.sleep(1.1)
    return lastScore,lastImg

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