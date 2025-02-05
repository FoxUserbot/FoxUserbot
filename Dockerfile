FROM ubuntu:latest

WORKDIR /Foxuserbot
COPY . /Foxuserbot

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN venv/bin/pip install kurigram
RUN chmod +x /Foxuserbot/run_docker.sh


CMD ["/bin/bash", "-c", "/Foxuserbot/run_docker.sh && venv/bin/python main.py"]
