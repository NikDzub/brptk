#!/bin/bash

CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "Start: $CURRENT_TIME"

CURRENT_DIR=$(pwd)

while true; do
    python3 $CURRENT_DIR/01_get_vids/z_from_brwsr.py 3 2 # (# brwsrs) (# new vids)
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    fi

    python3 $CURRENT_DIR/02_comment/z_comment.py 127.0.0.1:6555 # M2 (# comments)
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    fi

    python3 $CURRENT_DIR/03_likes/z_likes.py 127.0.0.1:6562 
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    fi
    # break
done