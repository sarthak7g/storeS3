FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN  python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

# LABEL maintainer='pythonMicroservice <sarthak@rklick.com>' \
# 	version='1.0'

CMD flask run --host=0.0.0.0 --port=5000
