import pymongo 

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
    imageCollection.insert_one({
        "scores":scores,
        "insert_date":str(datetime.datetime.now()),
        "image":imgBytes
    }
)