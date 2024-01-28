#!/bin/bash
# This script sets up the virtual environment for the project
# @author KOOKIIE

VENV_PATH="$PWD/venv"
echo "Setting up virtual environment, please wait!"
echo "Do not close this window until you are told to do so!"

echo "Generating venv folder..."
python3 -m venv "$VENV_PATH"

echo "Installing dependencies..."
source "$PWD"/venv/bin/activate

pip install wheel
pip install -r requirements.txt
echo "Sequence completed! You may now close this window:"
exit