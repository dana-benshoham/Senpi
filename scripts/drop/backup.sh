#!/usr/bin/env bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <src_folder> <dest_folder>"
    exit 1
fi

# Variables
SRC_FOLDER="$1"
DEST_FOLDER="$2"

cd $DEST_FOLDER
mkdir Backup
cd Backup
cp "$SRC_FOLDER/app.log" app.log 
cp "$SRC_FOLDER/bootlaoder.log" bootloader.log 
cp "$SRC_FOLDER/FPGA" . -r 