FROM ubuntu:latest

WORKDIR /Foxuserbot
COPY . /Foxuserbot

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv nodejs npm
RUN npm install -g localtunnel
RUN python3 -m venv venv

CMD ["venv/bin/python", "main.py"]
