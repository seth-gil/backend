# Database setup

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

mdb = client["mdb"]
mdb["projects"].drop()
projects = mdb["projects"]