from app import app

from flask import render_template, redirect, request, send_file, send_from_directory, abort, jsonify
from flask.helpers import safe_join
import os
from werkzeug.utils import secure_filename
import base64

app.config["file_uploads"] = "app/static/"
app.config["Allowed_extensions"] = ["PNG", "JPG", "JPEG", "GIF", "MP4", "DOCX", "PDF","WEBM","MKV", "BLOB"]

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

        if "contact_name" and "contact_email" in request.args:
            email_val = request.args["contact_email"]
            name_val = request.args["contact_name"]
            print(request.args["contact_name"], request.args["contact_email"])
        
            if request.files:

                uploadFile = request.files['filename']

                if uploadFile.filename == "":
                    print("File must have a filename")
                    return jsonify("File must have a filename")

                if not allowedFile(uploadFile.filename):
                    if uploadFile.filename.upper()=="BLOB":
                        video_stream = uploadFile.read()
                        with open(os.path.join(app.config['file_uploads'], f"{name_val}_file.webm"), 'wb') as f_vid:
                            f_vid.write(video_stream)
                            f_vid.close()

                        return jsonify("success")

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
            filename_new = safe_join(app.root_path, "static", file_name)

            if os.path.isfile(filename_new):
                try:
                    return send_file(filename_new)
                except Exception as e: 
                    return jsonify(f"your path exists with error:{e}")
            else:
                return jsonify(f"{filename_new} does not exists")

    return render_template("index.html")

@app.route("/download-file", methods=["GET"])
def download_file():
    if request.method == "GET":
        if "file_name" in request.args:
            file_name = request.args["file_name"]
            filename_new = safe_join(app.root_path, "static", file_name)

            if os.path.isfile(filename_new):
                try:
                    return send_file(filename_new, as_attachment=True)
                except Exception as e: 
                    return jsonify(f"your path exists with error:{e}")
            else:
                return jsonify(f"{filename_new} does not exists")
