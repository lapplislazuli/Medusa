import pymongo 
from PIL import Image
import datetime
import io

################# Mongo Helpers #######################

uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"

# Used in Medusa - Training
def getMedusaTrainingCollection():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    TrainingCollection = medusaDB["StratifiedTraining"]
    return TrainingCollection

def getMedusaTestCollection():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    TestCollection = medusaDB["StratifiedTest"]
    return TestCollection

def getMedusaImageCollection():
    mongoClient=pymongo.MongoClient(uri)
    medusaDB = mongoClient["Medusa"]
    Images = medusaDB["Images"]
    return Images

def get_Image_cursor(collection):
    cursor = collection.find()
    return cursor

def get_next_n_samples(cursor,n = 100):
    samples = []
    for _ in range(n):
        entry = cursor.next()
        samples.append((entry["success"],entry["image"]))
    return samples

# Used in Scorer
def save_results_to_Mongo(scores,imgBytes):
    images = getMedusaImageCollection()
    images.insert_one({
        "scores":scores,
        "insert_date":str(datetime.datetime.now()),
        "image":imgBytes
    }
)

def create_img_from_mongoDBBytes(mongobytes, colorscheme='RGBA'):
    image = Image.open(io.BytesIO(mongobytes))
    return image