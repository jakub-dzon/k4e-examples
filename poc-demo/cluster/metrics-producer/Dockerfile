FROM python:3.9-slim-buster

RUN mkdir /code
WORKDIR /code

RUN python3.9 -m pip install boto3 prometheus-client

COPY metrics-producer.py .

CMD ["python3.9", "metrics-producer.py"]