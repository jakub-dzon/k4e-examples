#!/bin/bash

xargs -I'{}' oc label edgedevice {} dc=$2 <$1