from app import app

from flask import render_template, redirect, request
import os
from werkzeug.utils import secure_filename


app.config["file_uploads"] = "E:\\storeS3\\app\\static\\img"
app.config["Allowed_extensions"] = ["PNG", "JPG", "JPEG", "GIF", "MP4", "DOCX", "PDF"]

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
                return redirect(request.url)

            if not allowedFile(uploadFile.filename):
                print("That files extensions are not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(uploadFile.filename)
                uploadFile.save(os.path.join(app.config['file_uploads'], filename))
            print("file saved")
            return redirect(request.url)


    return render_template("index.html")