import numpy as np
from PIL import Image
import time

import Scorer as Scorer
import ImageHelper as ImgHelper
import MedusaMongo as MMongo

from scipy import ndimage

################### Helpers #####################


# Composes f(x)&g(x) -> f(g(x))
_compose = lambda g,h : lambda x : g(h(x))

# This methods sticks multiple alternation-functions to one
# Every method needs to be a monad, exactly taking one image and returning one image
def chain(fns):
    neutral = lambda x : x 
    for f in fns:
        neutral = _compose(neutral,f)
    return neutral

# Uses a model and predicts a single image
# This should be somewhere around, actually? 
def predict_single_image(model,img):
    imgArr = (np.expand_dims(img,0)) # Keras Models want to batch-predict images. Therefore we create a single element array
    imgArr = imgArr/255 # Aphrodite was trained with Values normed [0,1]
    return model.predict(imgArr)[0],img

############## Alternation Bricks #######################
# Takes an image, and puts some noise on it. 
# Return the image
def _noise(image):
    noise = _generate_noise(0.5,8)
    altered = image+noise
    return altered

def _softNoise(image):
    noise = _generate_noise(0.4,4)
    altered = image+noise
    return altered

def _spareStrongNoise(image):
    noise = _generate_noise(0.2,30)
    altered = image+noise
    return altered

def _normalize(image):
    # Image must be reparsed in the valid data-range [0,255]
    # Values smaller than 0 will be mapped to high values (e.g. -2 => 253)
    return np.asarray(image,dtype="uint8")

# Takes an image and smooths it with gaussian filter
def _smooth(image):
    #Sigma = 2 often is too strong, doesnt yield to good results IMO
    return ndimage.filters.gaussian_filter(image,2)

# Takes an image, puts noise on it, and smooths it with gaussian filter
def _softSmooth(image):
    # The Gaussian filter is quite strong, so i've taken only a little sigma
    altered = ndimage.filters.gaussian_filter(image,0.5)
    return altered

# Sharpes an edge using unsharp masking 
# Does not work as intented with rgb!   
def _sharp(image):
    mask = image-_smooth(image)
    return image+mask*0.1

# brightens and image by increasing each colour value
def _brigten(image):
    return image+5

# Generates an (64x64x3) Image with small values. It can be subtracted/added to a normal image to noise it
# Could be moved to ImgHelper/Generator. Kept it here for a while so noone needs to search it. 
def _generate_noise(density,strength=10,width=64,height=64):
    noise = np.random.rand(width,height,3)
    noise -=0.5 # to run from [-0.5,0.5]
    noise = np.asarray([p if np.random.rand()<density else 0 for p in noise.ravel()]).reshape((width,height,3))
    noise*=strength # To have Values bigger than 1, everything else would dissapear
    noise = np.asarray(noise,dtype="int")
    return noise

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
def remoteDegenerate(image, alternationfn = _noise, decay = 0.01, iterations = 10, maxloops=2000, verbose=True, history=True):
    # First: Check if the Credentials are correct and the image is detected
    initialResp = Scorer.send_ppm_image(image)
    if(initialResp.status_code!=200):
        return
    # Initialise Start-Variables from our first score
    totalLoops = 0 #Counts all loops
    depth = 0 #Counts successfull loops
    lastImage = image
    lastScore = Scorer.get_best_score(initialResp.text)
    # To check if we put garbage in
    print("StartConfidence:",lastScore)

    if history:
        h = []    

    #We stop if we either reach our depth, or we exceed the maxloops
    while(depth<iterations and totalLoops<maxloops):
        totalLoops+=1
        # Alter the last image and score it
        degenerated = alternationfn(lastImage.copy())
        degeneratedResp = Scorer.send_ppm_image(degenerated)
        if (degeneratedResp.status_code==200):
          degeneratedScore= Scorer.get_best_score(degeneratedResp.text)
          # if we verbose, we want console output (then we see directly if anything is not working, e.g. a to strong alternationfn)
          if verbose:
            print("Score:",degeneratedScore,"Depth:",depth, "Loop:" , totalLoops)
          # if we have history=True, we collect the same data as in verbose to plot something nice
          if history:
              h.append((degeneratedScore,depth,totalLoops))
          # If our score is acceptable (better than the set decay) we keep the new image and score
          if(degeneratedScore> lastScore-decay):
              lastImage=degenerated
              lastScore=degeneratedScore
              depth+=1
        else:
          print("Error, status code was: ", degeneratedResp.status_code)
          #Attempts do not count
          totalLoops-=1
       
        #We are working remote, we need to take a short break
        time.sleep(1.1)
    #We return the lastImg, this can be something not that good if we just reach maxloops!
    if h!=[] :
        return lastScore,lastImage,h
    else:
        return lastScore,lastImage

################### Local ######################
# This Degeneration runs for local Models
# Procedere is nearly the same as above
def degenerate (model, image, label, alternationfn = _noise, iterations=10, decay = 0.01, maxloops=2000,verbose=False,history=True):
    totalLoops = 0
    depth = 0
    lastScores,lastImage = predict_single_image(model,image)
    lastLabelScore=lastScores[label]

    # To check if we put garbage in
    print("StartConfidence:",lastLabelScore)

    if history:
        h = []

    while(depth<iterations and totalLoops<maxloops):
        totalLoops+=1
        degenerated = alternationfn(lastImage.copy())
        degScores,degImage = predict_single_image(model,degenerated)
        degLabelScore=degScores[label]

        if verbose:
            print("Score:",degLabelScore,"Depth:",depth, "Loop:" , totalLoops)
        if history:
            h.append((degLabelScore,depth,totalLoops))

        if(degLabelScore> lastLabelScore-decay):
            lastImage=degImage
            lastLabelScore=degLabelScore
            depth+=1
    if h!=[] :
        return lastLabelScore,lastImage,h
    else:
        return lastLabelScore,lastImage