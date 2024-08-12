#!/bin/bash

CURRENT_DIR=$(pwd)
FILE_TO_MONITOR="$CURRENT_DIR/01_get_vids_loop/etc/videos_new.txt"
MIN_LINES=5


get_line_count() {
    wc -l < "$FILE_TO_MONITOR"
}

while true; do
    LINE_COUNT=$(get_line_count)
    CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")


    if [ "$LINE_COUNT" -gt "$MIN_LINES" ]; then
        printf "$LINE_COUNT/$MIN_LINES $CURRENT_TIME"

        python3 $CURRENT_DIR/zz_uiauto.py
        if [ $? -ne 0 ]; then
            echo "zz_uiauto.py failed."
            continue
        fi

        # COMMENT ON ALL
        python3 $CURRENT_DIR/02_comment_loop/z_comment.py
        if [ $? -ne 0 ]; then
            echo "02_comment_loop/z_comment.py failed."
            continue
        fi

        python3 $CURRENT_DIR/03_likes/z_fix_urls.py
        if [ $? -ne 0 ]; then
            echo "z_fix_urls.py failed."
            continue
        fi
        
        # LIKE ALL    
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
