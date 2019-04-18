# Main Flask container

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import cv2
import pymongo

app = Flask(__name__, static_folder='/')
CORS(app);

# Animates all files in a folder 
def AnimateFolder(imgFolder,video):
	images = [img for img in os.listdir(imgFolder) if img.endswith(".jpg")]
	frame = cv2.imread(os.path.join(imgFolder, images[0]))
	height, width, layers = frame.shape

	vidPathA = os.path.join(imgFolder,video+".avi")
	vidPathM = os.path.join(imgFolder,"preview"+".mp4")

	video = cv2.VideoWriter(vidPathA, 0, 1, (width,height))

	for image in images:
		video.write(cv2.imread(os.path.join(imgFolder, image)))

	video.release()

	os.system("ffmpeg -i " + vidPathA + " " + vidPathM)
	os.remove(vidPathA)
	return vidPathM


@app.route("/api/v1/upload",methods=["POST"])
def Animate():
	print(request.form["id"])

	task_id = request.form["id"]
	try:
		request.files
		None
	except:
		abort(400)
	if not os.path.exists(task_id):
		os.makedirs(task_id)

	i = 0
	for file in request.files.getlist("files[]"):
		file.save(os.path.join(task_id,str(i)+".jpg"))
		i = i+1
	print("\n\n\n"+str(request.files.getlist("request"))+"\n\n\n")

	AnimateFolder(task_id,task_id)
	return ("success")

@app.route("/api/v1/project/<string:project_id>",methods=["GET"])
def project(project_id):
	name = "NamePlaceholder"
	desc = "DescPlaceholder"
	thumb = "default/1.jpg"
	return jsonify({"name":name,"description":desc,"thumbnail":thumb,"id":"default"})

@app.route("/api/v1/test",methods=["GET"])
def test():
	return "success"

# Any non API requests ~ Gil
@app.route('/', defaults={'path': 'root'})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        abort(404)

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)  # delet when deploying
