#!/bin/bash

if ! snapctl is-connected network-control; then
        echo "The network-control interface is not connected!"
        echo "Please run the following command:"
        echo "    snap connect ${SNAP_NAME}:network-control"
        exit 0
fi

for f in enP4p65s0 enP3p49s0; do
        echo "Disabling network interface offload functionality for ${f}"
        ${SNAP}/sbin/ethtool -K "${f}" tso off gro off gso off tx off rx off
done
