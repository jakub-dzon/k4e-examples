#!/bin/bash

oc patch edgedevice $1 --type='json' -p '[{"op": "add", "path": "/spec/heartbeat", "value": {"periodSeconds": 5}}]'