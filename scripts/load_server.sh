#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")

$SCRIPT_DIR/../sensei_server/venv/bin/python $SCRIPT_DIR/../sensei_server/check_server.py
