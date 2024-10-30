#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <src_folder> <dest_folder> <folder_name>"
    exit 1
fi

# Variables
SRC_FOLDER="$1"
DEST_FOLDER="$2"
FOLDER_NAME="$3"

# Copy Drop From DoK to Local Documents
cp $SRC_FOLDER $DEST_FOLDER -r

# Navigate to the destination folder
pushd $DEST_FOLDER/$FOLDER_NAME

# Create a virtual environment in the destination folder
python3 -m venv app_venv

# Activate the virtual environment
source "app_venv/bin/activate"

# Install the requirements from the requirements.txt file
pip install -r requirements.txt
popd
echo "Installation completed!"