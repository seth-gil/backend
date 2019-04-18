# Database setup

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

mdb = client["mdb"]
projects = mdb["mdb"]

sample {"_id":"default",
		"name":"name",
		"description":"Sample project",
		"Thumbnail":"root/default/1.jpg"}

projects.insert_one(sample)