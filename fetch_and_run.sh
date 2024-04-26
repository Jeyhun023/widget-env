#!/bin/bash
MAIN_DIR=/usr/src/app
WIDGET_DIR=$MAIN_DIR/widget

# for var in $(compgen -e); do
#     export "$var"
# done

# Download python packages
pip install -r $WIDGET_DIR/requirements.pip

# Download system packages
apt-get update
xargs apt-get -y install < $WIDGET_DIR/requirements.system

# Run the Python script
cd $WIDGET_DIR
python3.10 $WIDGET_DIR/run.py

# List output
cd $WIDGET_DIR/output
ls -la
