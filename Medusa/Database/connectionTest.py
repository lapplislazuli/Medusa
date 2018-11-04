import pymongo 
from PIL import Image
import numpy as np
import io
#User: MedusaUser
#PW: P3R5EU? 
#Maybe ... maybe the '?' could cause trouble 

uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"

def getMedusaImageCollection():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    imageCollection = medusaDB["Images"]
    return imageCollection

def testInsert():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    testCollection = medusaDB["Testitems"]
    testCollection.insert_one({"name":"Test1", "something":2})

def testGet():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    testCollection = medusaDB["Testitems"]
    item = testCollection.find_one()
    print(item)

def getOneImage():
    imageCollection = getMedusaImageCollection()
    item = imageCollection.find_one()
    return item

def get_Image_cursor():
    imageCollection = getMedusaImageCollection()
    items = imageCollection.find()
    return items

def create_img_from_mongoDBBytes(mongobytes, colorscheme='RGBA'):
    image = Image.open(io.BytesIO(mongobytes))
    return image

def get_next_n_samples(n = 100):
    cursor = get_Image_cursor()
    samples = []
    for _ in range(n):
        entry = cursor.next()
        samples.append((entry["success"],entry["image"]))
    print(len(samples))

get_next_n_samples()
