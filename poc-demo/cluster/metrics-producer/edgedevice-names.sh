#!/bin/bash

oc get edgedevice -ojsonpath="{range .items[*]}{.metadata.name}{'\n'}" > $1