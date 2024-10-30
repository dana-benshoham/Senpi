#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
SENPI_DIR=$SCRIPT_DIR/../
DROP_DIR=Sensei_app

pushd $SENPI_DIR

rm -rf $DROP_DIR
mkdir $DROP_DIR
cp src/ $DROP_DIR -r
cp FPGA/ $DROP_DIR -r
mkdir $DROP_DIR/scripts
cp scripts/drop/* $DROP_DIR/scripts/ -r
cp version.json $DROP_DIR
cp requirements.txt $DROP_DIR
cp tests/ $DROP_DIR -r
popd
ls "$SENPI_DIR/$DROP_DIR" -l