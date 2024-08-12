#!/bin/bash

CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
CURRENT_DIR=$(pwd)
BRWSRS=$1

while true; do
    echo "search videos loop started: $CURRENT_TIME"
    python3 "$CURRENT_DIR/01_get_vids_loop/in_loop.py" "$BRWSRS"
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    echo "ended script."
    fi

done