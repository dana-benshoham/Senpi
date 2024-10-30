#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <app_folder>"
    exit 1
fi

# Variables
APP_PATH="$1"
FPGA_BIN_NAME = "b205_dummy3.bin"

sudo uhd_find_devices
cp "$APP_PATH/FPGA/$FPGA_BIN_NAME" "/usr/local/share/uhd/images/"
sudo sudo uhd_image_loader --args="type=b200" --fpga-path="/usr/local/share/uhd/images/$FPGA_BIN_NAME"

"$APP_PATH/app_venv/bin/python" "$APP_PATH/src/main.py"