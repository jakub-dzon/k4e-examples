import datetime
import os
import time

import boto3
from prometheus_client import start_http_server, Gauge

start_http_server(8081)

device_id = os.getenv("DEVICE")
endpoint_url = "https://" + os.getenv("BUCKET_HOST")
bucket_name = os.getenv("BUCKET_NAME")
gauges = {}

last_time = None
while True:
    s3 = boto3.resource('s3', endpoint_url=endpoint_url, verify=False)
    bucket = s3.Bucket(bucket_name)
    latest_time = last_time
    for my_bucket_object in bucket.objects.filter(Prefix="statistics").all():
        file_key = my_bucket_object.key
        segments = str.split(file_key, "/")
        date_time_obj = datetime.datetime.strptime(segments[1], '%Y-%m-%d_%H-%M-%S')

        if last_time is not None and date_time_obj <= last_time:
            continue

        if latest_time is None or date_time_obj > latest_time:
            latest_time = date_time_obj
        data = my_bucket_object.get()['Body']

        for line in data.iter_lines():
            name, var = line.decode("utf-8").partition("=")[::2]
            gauge_name = name + "_percent"
            gauge = gauges.get(gauge_name)
            if gauge is None:
                gauge = Gauge(gauge_name, name, ['device_id'])
                gauges[gauge_name] = gauge

            gauge.labels(device_id).set(var)

    last_time = latest_time
    time.sleep(10)
