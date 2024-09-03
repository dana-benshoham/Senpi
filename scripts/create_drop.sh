#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
SENPI_DIR=$SCRIPT_DIR/../
DROP_DIR=$SENPI_DIR/Sensei_app

pushd $SENPI_DIR

mkdir $DROP_DIR
cp src/ $DROP_DIR -r
cp version.json $DROP_DIR
cp requirements.txt $DROP_DIR
cp $SCRIPT_DIR/install_app.sh $DROP_DIR
cp tests/ $DROP_DIR -r

ls $DROP_DIR -l