#FROM python:alpine
FROM python:3.7.3-stretch

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip python-dev libogg0 libopus0 opus-tools ffmpeg
#RUN apk add ffmpeg python-dev opus make
#RUN apk add make

COPY requirements.txt requirements.txt
COPY main.py main.py

RUN pip install -r requirements.txt

CMD ["python", "/app/main.py"]