#!/usr/bin/env bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <src_folder> <dest_folder>"
    exit 1
fi

# Variables
SRC_FOLDER="$1"
DEST_FOLDER="$2"

$BACKUP_FOLDER = $DEST_FOLDER/Backup
mkdir $BACKUP_FOLDER
cp $SRC_FOLDER/app.log $BACKUP_FOLDER/app.log 
cp $SRC_FOLDER/bootlaoder.log $BACKUP_FOLDER/bootloader.log 
cp $SRC_FOLDER/FPGA $BACKUP_FOLDER/FPGA -r 