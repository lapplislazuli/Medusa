import pymongo 
from PIL import Image
import datetime
import io

import ImageHelper as ImgHelper

################# Mongo Helpers #######################

uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"

#Helper for fetching Medusa Mongo Collections
def getMedusaMongoCollection(collectionName):
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    Collection = medusaDB[collectionName]
    return Collection

# Used in Medusa - Training
def getMedusaTrainingCollection():
    return getMedusaMongoCollection('Training')

def getMedusaTestCollection():
    return getMedusaMongoCollection('Test')

def getMedusaImageCollection():
    return getMedusaMongoCollection('Images')

def getMedusaStrongImageCollection():
    return getMedusaMongoCollection("StrongImages")

def get_Image_cursor(collection):
    cursor = collection.find()
    return cursor

def get_next_n_samples(cursor,n = 100):
    samples = []
    for _ in range(n):
        entry = cursor.next()
        samples.append((entry["success"],entry["image"]))
    return samples

def get_image_of_collection(collectionName, imageNumber):
    collection = getMedusaMongoCollection(collectionName)
    cursor = get_Image_cursor(collection)
    data = get_next_n_samples(cursor, imageNumber)
    image = ImgHelper.create_img_from_mongoDBBytes(data[imageNumber][1])
    return image

# Used in Scorer
def save_results_to_Mongo(scores,imgBytes):
    images = getMedusaImageCollection()
    images.insert_one({
        "scores":scores,
        "insert_date":str(datetime.datetime.now()),
        "image":imgBytes
    }
)

