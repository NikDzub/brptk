#!/bin/bash

CURRENT_DIR=$(pwd)
DEVICE=$1

while true; do
    CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
    echo "search videos and comment loop started: $CURRENT_TIME"

    python3 $CURRENT_DIR/zz_uiauto_specific.py $DEVICE
    python3 "$CURRENT_DIR/01_get_vids_loop/from_device.py" "$DEVICE"
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    echo "ended script."
    fi

done