import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

mdb = client["mdb"]
projects = mdb["projects"]

for x in projects.find():
	print(x)