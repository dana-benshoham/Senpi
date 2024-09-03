#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")

cp $SCRIPT_DIR/sensei.service /etc/systemd/system/sensei.service

sudo systemctl daemon-reload

sudo systemctl enable sensei.service

sudo systemctl start sensei.service

sudo systemctl status sensei.service