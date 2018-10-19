import pymongo 

#User: MedusaUser
#PW: P3R5EU? 
#Maybe ... maybe the '?' could cause trouble 

uri = "mongodb://MedusaUser:P3R5EU?@applis.me/Medusa?authSource=Medusa"

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

testGet()