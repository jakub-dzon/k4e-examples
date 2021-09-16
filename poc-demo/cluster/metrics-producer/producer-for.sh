#!/usr/bin/bash

mkdir -p out

sed "s#@DEVICE_ID@#$1#g" metrics-producer.yaml > out/metrics-producer-$1.yaml