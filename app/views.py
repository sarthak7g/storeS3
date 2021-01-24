from app import app
from datetime import datetime
import requests
from flask import render_template, redirect, request, send_file, send_from_directory, abort, jsonify
from flask.helpers import safe_join
import os
from werkzeug.utils import secure_filename
import base64, json

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

        if "contact_name" and "contact_email" and "uuid" in request.args:
            email_val = request.args["contact_email"]
            name_val = request.args["contact_name"]
            uuid = request.args["uuid"]
        
            if request.files:

                uploadFile = request.files['filename']

                if uploadFile.filename == "":
                    print("File must have a filename")
                    return jsonify("File must have a filename")

                if not allowedFile(uploadFile.filename):

                    # only blob
                    if uploadFile.filename.upper()=="BLOB":
                        video_stream = uploadFile.read()
                        with open(os.path.join(app.config['file_uploads'], f"{uuid}_file.webm"), 'wb') as f_vid:
                            f_vid.write(video_stream)
                            f_vid.close()

                        # send to kafka
                        file_url = safe_join(app.root_path, "static", f"{uuid}_file.webm")
                        sendtoKafka(file_url, uuid, email_val)
                        return jsonify("success")

                    print("That files extensions are not allowed")
                    return jsonify("That files extensions are not allowed")
                else:
                    ext = uploadFile.filename.rsplit(".", 1)[1]
                    uploadFile.save(os.path.join(app.config['file_uploads'], f'{uuid}_file.{ext}'))

                    # send to kafka
                    file_url = safe_join(app.root_path, "static", f'{uuid}_file.{ext}')
                    print(file_url)
                    sendtoKafka(file_url, uuid, email_val)

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

def sendtoKafka(video_url, uuid, email):

        url = "https://kong.princetonhive.com/api/Webhooks/Webhooks"
        version = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        payload = {
            "VideoURL": video_url,
            "UUID": uuid,
            "Email": email,
            "CourseId": 11111111,
            "LessonId": 11111111,
            "Version": version,
            "B2bdomain": "null",
            "reqId": "1c58845f-7b1f-4124-9c4b-841aba91af07"
        }

        headers = {
        'Content-Type': 'application/json'
        }
        print(json.dumps(payload))
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        print(response)



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

