#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <app_folder>"
    exit 1
fi

# Variables
APP_PATH="$1"
FPGA_BIN_NAME="usrp_b205mini_fpga.bin"
FPGA_FW_NAME="usrp_b200_fw.hex"

sudo uhd_find_devices
sudo cp "$APP_PATH/FPGA/$FPGA_BIN_NAME" "/usr/local/share/uhd/images/"
sudo cp "$APP_PATH/FPGA/$FPGA_FW_NAME" "/usr/local/share/uhd/images/"
sudo uhd_usrp_probe --args "master_clock_rate=40e6"
# Activate the virtual environment
# source "$APP_PATH/app_venv/bin/activate"

$APP_PATH/app_venv/bin/python "$APP_PATH/src/main.py"