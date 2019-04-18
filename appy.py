# Main Flask container

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import cv2
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps

# Flask setup
app = Flask(__name__, static_folder='root/')
CORS(app);

# Mongodb setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
mdb = client["mdb"]
projects = mdb["projects"]

# Animates all files in a folder 
def AnimateFolder(imgFolder,video):
	images = [img for img in os.listdir(os.path.join("root",imgFolder)) if img.endswith(".jpg")]
	frame = cv2.imread(os.path.join("root",imgFolder, images[0]))
	height, width, layers = frame.shape

	vidPathA = os.path.join("root",imgFolder,video+".avi")
	vidPathM = os.path.join("root",imgFolder,"preview"+".mp4")

	video = cv2.VideoWriter(vidPathA, 0, 1, (width,height))

	for image in images:
		video.write(cv2.imread(os.path.join("root",imgFolder, image)))

	video.release()

	os.system("ffmpeg -i " + vidPathA + " " + vidPathM)
	os.remove(vidPathA)
	return vidPathM

@app.route("/api/v1/project",methods=["POST"])
def NewProject():

	name = request.json["name"]
	desc = request.json["description"]

	print ("hello world")
	print (name,desc)

	newprj = {"name":name,
			  "description":desc,
			  "thumbnail":None}

	task_id = projects.insert(newprj)

	# try: print (task_id)
	# except: print("1")
	# try: print (task_id.inserted_id)
	# except: print("1")
	# try: print (task_id.str)
	# except: print("1")
	# try: print (str(task_id))
	# except: print("1")

	return str(task_id)

@app.route("/api/v1/upload",methods=["POST"])
def Animate():

	task_id = request.form["id"]
	try:
		request.files
		None
	except:
		abort(400)

	if not os.path.exists("root/"+task_id):
		os.makedirs("root/"+task_id)

	i = 0
	for file in request.files.getlist("files[]"):
		file.save(os.path.join("root",task_id,str(i)+".jpg"))
		i = i+1

	AnimateFolder(task_id,task_id)

	return (task_id)

@app.route("/api/v1/project/<string:project_id>",methods=["GET"])
def project(project_id):
	print (ObjectId(project_id))
	myquery = {"_id":ObjectId(project_id)}

	ret = projects.find(myquery)

	return dumps(ret[0])

@app.route("/api/v1/test",methods=["GET"])
def test():
	return "success"

# Any non API requests ~ Gil
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return "404: File not found at " + path + " as of now.";

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)  # delet when deploying
