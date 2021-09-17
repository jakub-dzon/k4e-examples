#!/bin/bash

oc get edgedevice -ojsonpath="{range .items[*]}{.metadata.name}{'\n\t'}{range .status.deployments[*]}{.name}{':\t'}{.phase}{'\n\t'}{end}{'\n'}{end}"