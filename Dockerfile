FROM ubuntu:latest

ENV DOCKER=True

WORKDIR /Foxuserbot
COPY . /Foxuserbot

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv wget unzip curl openssh-client
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip

EXPOSE 8080

CMD ["venv/bin/python", "main.py"]
