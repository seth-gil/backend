# Main Flask container

from flask import Flask, send_from_directory, request
from flask_cors import CORS
import os
import cv2
import pymongo
import base64
import json
import re
from bson.objectid import ObjectId
from bson import json_util
from PIL import Image
from io import BytesIO


# Flask setup
app = Flask(__name__, static_folder='root/')
CORS(app);

# Mongodb setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
mdb = client["mdb"]
projects = mdb["projects"]

# Animates all files in a folder 
def AnimateFolder(imgFolder,video,rate):
	images = [img for img in os.listdir(os.path.join("root",imgFolder)) if img.endswith(".jpg")]

	vidPathA = os.path.join("root",imgFolder,video+".avi")
	vidPathM = os.path.join("root",imgFolder,"preview"+".mp4")

	# for item in os.listdir(os.path.join("root",imgFolder)):
	# 	print (item)
	# 	if os.path.isfile(os.path.join("root",imgFolder,item)):
	# 		im = Image.open(os.path.join("root",imgFolder,item))
	# 		imResize = im.resize((200,200), Image.ANTIALIAS)
	# 		imResize.save(os.path.join("root",imgFolder,item))

	# images = [img for img in os.listdir(os.path.join("root",imgFolder)) if img.endswith(".jpg")]
	frame = cv2.imread(os.path.join("root",imgFolder, images[0]))
	height, width, layers = frame.shape

	video = cv2.VideoWriter(vidPathA, 0, rate, (width,height))

	for image in images:
		video.write(cv2.imread(os.path.join("root",imgFolder,image)))

	video.release()

	os.system("ffmpeg -y -i " + vidPathA + " " + vidPathM) #-b:v 2500k 
	os.remove(vidPathA)
	return vidPathM

@app.route("/api/v1/project",methods=["POST"])
def NewProject():

	#print (request.json)

	name = request.json["name"]
	desc = request.json["description"]
	rate = request.json["framerate"]
	frames = request.json["frames"]

	newprj = {"name":name,
			  "description":desc}

	task_id = projects.insert(newprj)
	task_id = str(task_id)

	print("\nNew project created\nName:%s\nDescription:%s\nFramerate:%s\nID:%s\n\n" % (name,desc,rate,task_id))

	try:
		request.files
		None
	except:
		abort(400)

	if not os.path.exists("root/"+task_id):
		os.makedirs("root/"+task_id)

	# i = 0
	# for file in request.files.getlist("files[]"):
	# 	file.save(os.path.join("root",task_id,str(i)+".jpg"))
	# 	i = i+1

	i = 0
	for frame in frames:
		try: print (frame[:20])
		except: print (frame)
		image_data = re.sub('^data:image/.+;base64,', '', frame)
		#print (image_data[20:])
		im = Image.open(BytesIO(base64.b64decode(image_data)))
		im.save(os.path.join("root",task_id,str(i)+".jpg"))
		i = i+1

	AnimateFolder(task_id,task_id,int(rate))

	return task_id

@app.route("/api/v1/project/<string:project_id>",methods=["GET"])
def project(project_id):
	query = {"_id":ObjectId(project_id)}

	ret = projects.find(query)

	niceRet = ret[0]
	niceRet["_id"] = str(ret[0]["_id"])

	return json.dumps(niceRet)

@app.route("/api/v1/test",methods=["GET"])
def test():
	return "success"

@app.route("/api/v1/projects",methods=["GET"])
def returnAll():
	ret = projects.find()
	print (ret)

	#return json.dumps(ret, sort_keys=True, default=json_util.default)
	return "please let the suffering end"

# Any non API requests ~ Gil
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return "404: File not found at " + path + " as of now.";

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)
