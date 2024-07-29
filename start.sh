#!/bin/bash

CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")

# echo "Start: $CURRENT_TIME"

CURRENT_DIR=$(pwd)

while true; do
    echo "Start 01: $CURRENT_TIME"
    timeout 700 python3 $CURRENT_DIR/01_get_vids/z_from_brwsr.py 4 5 # (# brwsrs) (# new vids)
    if [ $? -ne 0 ]; then
        echo "1failed, restarting..."
        continue
    fi

    echo "Start 02: $CURRENT_TIME"
    python3 $CURRENT_DIR/02_comment/z_comment.py 127.0.0.1:6555 # (# comments)
    if [ $? -ne 0 ]; then
        echo "2failed, restarting..."
        continue
    fi

    echo "Start 03: $CURRENT_TIME"
    python3 $CURRENT_DIR/03_likes/z_likes.py RF8MB29J8AE # 127.0.0.1:6562 
    if [ $? -ne 0 ]; then
        echo "3failed, restarting..."
        continue
    fi
    # break
done