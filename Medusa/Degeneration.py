import numpy as np

import MedusaMongo as MMongo
import ImageGenerator as MImg

from PIL import Image
import time

import Scorer as Scorer
import ImageHelper as ImgHelper

############################### Remote #######################################
# This Methods runs Remote - the local Degeneration is Beneath

# Method requires: 
#   An image (as 64x64x3 Uint8 Array), 
#   a function to alter the image,
#   a threshhold how much the image can be worse by every step
#   The # of Iterations i want to (successfully) alter my image
#   The # of loops which i want to do max
# Scores an image, alters it, and keeps the altered image if its not that worse.
# Method Logic will be documented in detail throughout the function
def remoteDegenerate(image, alternationfn = _alterImage, decay = 0.01, iterations = 10, maxloops=2000):
    # First: Check if the Credentials are correct and the image is detected
    initialResp = Scorer.send_ppm_image(image)
    if(initialResp.status_code!=200):
        return
    # Initialise Start-Variables from our first score
    totalLoops = 0 #Counts all loops
    depth = 0 #Counts successfull loops
    lastImg = image
    lastScore = Scorer.get_best_score(initialResp.text)
    # To check if we put garbage in
    print("StartConfidence:",lastScore)

    #We stop if we either reach our depth, or we exceed the maxloops
    while(depth<iterations and totalLoops<maxloops):
        totalLoops+=1
        # Alter the last image and score it
        degenerated = alternationfn(lastImg.copy())
        degeneratedResp = Scorer.send_ppm_image(degenerated)
        degeneratedScore= Scorer.get_best_score(degeneratedResp.text)
        print("Score:",degeneratedScore,"Depth:",depth, "Loop:" , totalLoops)
        # If our score is acceptable (better than the set decay) we keep the new image and score
        if(degeneratedScore> lastScore-decay):
            lastImg=degenerated
            lastScore=degeneratedScore
            depth+=1
        #We are working remote, we need to take a short break
        time.sleep(1.1)
    #We return the lastImg, this can be something not that good if we just reach maxloops!
    return lastScore,lastImg
################### Local ######################
# This Degeneration runs for local Models
# Procedere is nearly the same as above

def degenerate(model, image, alternationfn = _alterImage, label, iterations=10, decay = 0.01, maxloops=2000):
    totalLoops = 0
    depth = 0
    lastScores,lastImage = predict_single_image(model,image)
    lastLabelScore=lastScores[label]
    
    while(depth<iterations and totalLoops<maxloops):
        totalLoops+=1
        degenerated = alternationfn(lastImage.copy())
        degScores,degImage = predict_single_image(model,degenerated)
        degLabelScore=degScores[label]
        if(degLabelScore> oldLabelScore-decay):
            lastImage=degImage
            lastLabelScore=degLabelScore
            depth+=1
    return lastLabelScore,lastImage

################### Helpers #####################

# Generates an (64x64x3) Image with small values. It can be subtracted/added to a normal image to noise it
# Could be moved to ImgHelper/Generator. Kept it here for a while so noone needs to search it. 
def _generate_noise(density,strength=10,width=64,height=64):
    noise = np.random.rand(width,height,3)
    noise -=0.5 # to run from [-0.5,0.5]
    noise*=strength # To have Values bigger than 1, everything else would dissapear
    noise = np.asarray(noise,dtype="int")
    return noise

# Takes an image, and puts some noise on it. 
# Return the image
def _alterImage(image,strength=8):
    noise = _generate_noise(0.5,strength)
    altered = image+noise
    # Image must be reparsed in the valid data-range [0,255]
    # Values smaller than 0 will be mapped to high values (e.g. -2 => 253)
    altered = np.asarray(altered,dtype="uint8")
    return altered

# Takes an image, puts noise on it, and smooths it with gaussian filter
def _alterImageWithSmooth(image,strength=25):
    noise = _generate_noise(0.5,strength)
    altered = image+noise
    # The Gaussian filter is quite strong, so i've taken only a little sigma
    altered = ndimage.filters.gaussian_filter(altered,2)
    altered = np.asarray(altered,dtype="uint8")
    return altered