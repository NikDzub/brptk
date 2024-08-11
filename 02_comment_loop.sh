#!/bin/bash

# Define paths and file to monitor
CURRENT_DIR=$(pwd)
FILE_TO_MONITOR="$CURRENT_DIR/01_get_vids_loop/etc/videos_new.txt"
MIN_LINES=5

# Function to get the number of lines in the file
get_line_count() {
    wc -l < "$FILE_TO_MONITOR"
}

while true; do
    LINE_COUNT=$(get_line_count)

    if [ "$LINE_COUNT" -gt "$MIN_LINES" ]; then
        echo "$LINE_COUNT/$MIN_LINES"

        # COMMENT ON ALL
        python3 $CURRENT_DIR/02_comment_loop/z_comment.py
        if [ $? -ne 0 ]; then
            echo "02_comment_loop/z_comment.py failed."
            continue
        fi
        
        # LIKE ALL    
        python3 $CURRENT_DIR/03_likes/z_likes.py RF8MB29J8AE
        if [ $? -ne 0 ]; then
            echo "03_likes/z_likes.py failed."
            continue
        fi        
    else
        echo "$LINE_COUNT/$MIN_LINES"

    fi
    
    # Wait for a specified interval before checking again
    sleep 20
done
