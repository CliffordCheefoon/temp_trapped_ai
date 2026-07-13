#!/bin/bash

# Start script for trapped_ai
echo "Starting trapped_ai..."

source .venv/bin/activate
pip install -r requirements.txt
python main.py