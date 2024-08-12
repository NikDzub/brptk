#!/bin/bash

CURRENT_DIR=$(pwd)
SERIAL=$1


run_script() {
    python3 "$CURRENT_DIR/frida_bypass.py" "$SERIAL" 
}

while true; do
    run_script
    echo "Restarting frida..."
    sleep 5
done
