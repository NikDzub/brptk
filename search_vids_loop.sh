#!/bin/bash

CURRENT_DIR=$(pwd)
BRWSRS=$1

while true; do
    CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
    echo "search videos loop started: $CURRENT_TIME"
    python3 "$CURRENT_DIR/01_get_vids_loop/in_loop.py" "$BRWSRS"
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    echo "ended script."
    fi

done