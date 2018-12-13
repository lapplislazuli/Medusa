import numpy as np
import tensorflow as tf
from tensorflow import keras
# our Bibs
import ImageGenerator as IG 

#### Loops ######
# Loops over the model until any class-confidence is higher than threshhold
def loop_until_threshhold(model,threshhold,batchsize=100):
    while True:
        batchScores,batchImages = create_and_rate_n_images(model,batchsize)
        bestScores,bestImage= get_highest_scoredBatchItem(batchScores,batchImages)
        bestClass,bestScore = get_highest_score_and_class(bestScores)
        print(bestScore)
        if (bestScore > threshhold):
            return bestClass , bestScore, bestImage
# Loops over the Model until there is a confidence for the label higher than threshhold
def loop_until_label_threshhold(model,label,threshhold,batchsize=100):
    while True:
        batchScores,batchImages = create_and_rate_n_images(model,batchsize)
        bestScore,bestImage= get_highest_scoredBatchItem_with_label(batchScores,batchImages,label)
        print(bestScore)
        if (bestScore > threshhold):
            return bestScore,bestImage

#### Rating #####
def create_and_rate_image(model):
    i = IG.create_image()
    img = (np.expand_dims(i,0))
    return model.predict(img),i

def create_and_rate_n_images(model,n=100):
    images = IG.create_n_images(n)
    scores = model.predict(images)
    return scores,images

###### Eval #####
def get_highest_score_and_class(scores):
    return np.argmax(scores),scores.max()

def get_highest_scoredBatchItem(scorebatch,imagebatch):
    index = 0
    bestScore=0
    for i in range(len(scorebatch)):
        if scorebatch[i].max() > bestScore:
            index=i
    return scorebatch[index],imagebatch[index]

def get_highest_scoredBatchItem_with_label(scorebatch,imagebatch,label):
    index = 0
    bestScore=0
    for i in range(len(scorebatch)):
        if scorebatch[i][label] > bestScore:
            index=i
            bestScore = scorebatch[i][label]
    return scorebatch[index][label],imagebatch[index]

# Uses a model and predicts a single image
def predict_single_image(model,img):
    imgArr = (np.expand_dims(img,0)) # Keras Models want to batch-predict images. Therefore we create a single element array
    imgArr = imgArr/255 # Aphrodite was trained with Values normed [0,1]
    return model.predict(imgArr)[0],img