#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dest_folder>"
    exit 1
fi

# Variables
SRC_FOLDER="$1"
DEST_FOLDER="$2"

# Copy Drop From DoK to Local Documents
cp $SRC_FOLDER $DEST_FOLDER -r

# Navigate to the destination folder
pushd $DEST_FOLDER

# Create a virtual environment in the destination folder
python3 -m venv app_venv

# Activate the virtual environment
source "app_venv/bin/activate"

# Install the requirements from the requirements.txt file
pip install -r requirements.txt
popd
echo "Installation completed!"