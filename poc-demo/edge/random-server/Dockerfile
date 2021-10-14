FROM python:3.9-slim-buster

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y python3-pip && pip3 install psutil cpu-load-generator

COPY random-server.py .

CMD ["python3", "random-server.py"]