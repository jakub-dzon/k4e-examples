import datetime
import os
import time

import boto3
from prometheus_client import start_http_server, Gauge

start_http_server(8081)

endpoint_url = "https://" + os.getenv("BUCKET_HOST")
bucket_name = os.getenv("BUCKET_NAME")
gauges = {}

last_time = None
while True:
    s3 = boto3.client('s3', endpoint_url=endpoint_url)

    latest_time = last_time
    result = s3.list_objects(Bucket=bucket_name, Prefix="statistics/", Delimiter="/")
    subfolders = set()
    for o in result.get('CommonPrefixes'):
        device_id_key = o.get('Prefix')
        subfolders.add(device_id_key)

    for folder in subfolders:
        result = s3.list_objects(Bucket=bucket_name, Prefix=folder, Marker=folder)
        contents = result.get('Contents')
        device_id = str.split(folder, "/")[1]
        if contents:
            for o in result.get('Contents'):
                file_key = o['Key']
                segments = str.split(file_key, "/")
                date_time_obj = datetime.datetime.strptime(segments[2], '%Y-%m-%d_%H-%M-%S')
                if last_time is not None and date_time_obj <= last_time:
                    continue

                if latest_time is None or date_time_obj > latest_time:
                    latest_time = date_time_obj
                data = s3.get_object(Bucket=bucket_name, Key=file_key)['Body']
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
