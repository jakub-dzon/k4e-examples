FROM python:3.9-slim-buster

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y python3-pip && pip3 install psutil

COPY stats.py .

CMD ["python3", "stats.py"]