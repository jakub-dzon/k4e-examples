FROM python:3.9-slim-buster

RUN mkdir /code
WORKDIR /code

RUN python3.9 -m pip install psutil cpu-load-generator
COPY random-server.py .

CMD ["python3.9", "random-server.py"]