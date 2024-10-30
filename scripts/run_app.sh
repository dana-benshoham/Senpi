#!/bin/bash

# Variables
APP_PATH="$1"
FGPA_BIN_NAME = "b205_dummy3.bin"

sudo uhd_find_devices
cp $APP_PATH/FPGA/$FGPA_BIN_NAME /usr/local/share/uhd/images/$FGPA_BIN_NAME
sudo sudo uhd_image_loader --args="type=b200" --fpga-path=/usr/local/share/uhd/images/$FGPA_BIN_NAME

$APP_PATH/app_venv/bin/python $APP_PATH/src/main.py