#!/bin/bash

# Get the directory of the Bash script
echo Start gateway backend
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Run Uvicorn for the main.py file with auto-reloading

cd ${SCRIPT_DIR}
source venv/bin/activate
gunicorn -b 0.0.0.0:5500 -w 1 --threads 3 main:app