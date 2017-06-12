FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip redis-server
RUN service redis-server start
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
