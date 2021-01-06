from app import app

from flask import render_template, redirect, request, send_file, send_from_directory, abort, jsonify
import os
from werkzeug.utils import secure_filename


app.config["file_uploads"] = "app\static\img"
app.config["get_file"] = "E:\storeS3\\app\static\img"
app.config["Allowed_extensions"] = ["PNG", "JPG", "JPEG", "GIF", "MP4", "DOCX", "PDF","WEBM"]

@app.route("/")
def index():
    return "<h1>Welcome to the store</h1>"


def allowedFile(filename):
    if not '.' in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["Allowed_extensions"]:
        return True
    return False


@app.route("/upload-file", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":

        if request.files:

            uploadFile = request.files['filename']

            if uploadFile.filename == "":
                print("File must have a filename")
                return jsonify("File must have a filename")

            if not allowedFile(uploadFile.filename):
                print("That files extensions are not allowed")
                return jsonify("That files extensions are not allowed")
            else:
                filename = secure_filename(uploadFile.filename)
                uploadFile.save(os.path.join(app.config['file_uploads'], filename))
            print("file saved")
            return jsonify("success")

    if request.method == "GET":
        if "file_name" in request.args:
            file_name=request.args["file_name"]
            abs_path = os.path.join(app.config['get_file'], file_name)
            
            if not os.path.exists(abs_path):
                return jsonify(f"{abs_path} does not exists")

            if os.path.isfile(abs_path):
                return send_file(abs_path)


    return render_template("index.html")