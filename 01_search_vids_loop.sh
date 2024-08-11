#!/bin/bash

CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
BRWSRS=$1


# echo "Start: $CURRENT_TIME"

CURRENT_DIR=$(pwd)


while true; do
    echo "search videos loop started: $CURRENT_TIME"
    python3 "$CURRENT_DIR/01_get_vids_loop/in_loop.py" "$BRWSRS"
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    echo "ended script."
    fi

done