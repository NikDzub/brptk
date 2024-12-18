#!/bin/bash

CURRENT_DIR=$(pwd)
FILE_TO_MONITOR="$CURRENT_DIR/02_comment_loop/etc/comment_url.txt"
MIN_LINES=3


get_line_count() {
    wc -l < "$FILE_TO_MONITOR"
}

while true; do
    LINE_COUNT=$(get_line_count)
    CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")


    if [ "$LINE_COUNT" -gt "$MIN_LINES" ]; then
        printf "$LINE_COUNT/$MIN_LINES $CURRENT_TIME"

        # UIAUTO
        python3 zz_uiauto_specific.py RF8MB29J8AE
        if [ $? -ne 0 ]; then
            echo "zz_uiauto_specific.py failed."
            continue
        fi
        
        # LIKE ALL 
        python3 $CURRENT_DIR/03_likes/z_fix_urls.py
        if [ $? -ne 0 ]; then
            echo "z_fix_urls.py failed."
            continue
        fi

        python3 $CURRENT_DIR/03_likes/z_likes.py RF8MB29J8AE
        if [ $? -ne 0 ]; then
            echo "03_likes/z_likes.py failed."
            continue
        fi        
    else
        printf "%s\r" "$LINE_COUNT/$MIN_LINES $CURRENT_TIME"

    fi
    
    sleep 2
done
