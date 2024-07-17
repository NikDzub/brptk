#!/bin/bash



while true; do
    python3 M1.py 4 1 # python3 M1 (# brwsrs) (# new vids)
    if [ $? -ne 0 ]; then
        echo "M1.py failed, restarting..."
        continue
    fi

    python3 M2.py 3 0 # python3 M2 (# comments)
    if [ $? -ne 0 ]; then
        echo "M2.py failed, restarting..."
        continue
    fi

    python3 M3.py 3 0 # python3 M3.py (# like brwsrs) (reply?blocked*)
    if [ $? -ne 0 ]; then
        echo "M2.py failed, restarting..."
        continue
    fi
    # break
done