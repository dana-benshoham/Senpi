#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dest_folder>"
    exit 1
fi

# Variables
DEST_FOLDER="$1"

# Navigate to the destination folder
pushd $DEST_FOLDER

# Create a virtual environment in the destination folder
python3 -m venv venv

# Activate the virtual environment
source "venv/bin/activate"

# Install the requirements from the requirements.txt file
pip install -r requirements.txt
popd
echo "Installation completed!"