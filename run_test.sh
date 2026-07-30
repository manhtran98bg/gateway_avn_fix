#!/bin/bash
# Get the directory of the Bash script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Run Uvicorn for the main.py file with auto-reloading
cd ${SCRIPT_DIR}
source ${SCRIPT_DIR}/venv/bin/activate
pytest ${SCRIPT_DIR}/test --html=report.html --self-contained-html
if [ "$1" == "--show" ]; then
    xdg-open ./report.html
fi