#!/usr/bin/env bash

# Variables
SRC_FOLDER="$1"
DEST_FOLDER="$2"

$BACKUP_FOLDER = $DEST_FOLDER/Backup
mkdir $BACKUP_FOLDER
cp $SRC_FOLDER/app.log $BACKUP_FOLDER/app.log 
cp $SRC_FOLDER/bootlaoder.log $BACKUP_FOLDER/bootloader.log 
cp $SRC_FOLDER/FPGA $BACKUP_FOLDER/FPGA -r 