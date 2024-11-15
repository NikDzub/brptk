#!/bin/bash

CURRENT_DIR=$(pwd)

while true; do
        python3 $CURRENT_DIR/03_likes_brw/z_likes.py 1
        if [ $? -ne 0 ]; then
            echo " failed."
            continue
        fi        
    
    sleep 2
done
