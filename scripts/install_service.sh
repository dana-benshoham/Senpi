#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")

cp $SCRIPT_DIR/sensei.service /etc/systemd/system/sensei.service
# Recognize new service
sudo systemctl daemon-reload

# Enable new service
sudo systemctl enable sensei.service

# Start new service
sudo systemctl start sensei.service

# Print new service status
sudo systemctl status sensei.service