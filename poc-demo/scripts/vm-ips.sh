#!/bin/bash

virsh net-dhcp-leases default | grep ipv4 | awk '{print $5}' | cut -d'/' -f 1