import logging
from app import APP_PATH
import os
from datetime import datetime
from app.internal.yaml_loader import LIMIT_LOGGER
from flask import send_file
from typing import Dict

__logging_folder_path: str = f'{APP_PATH}/resource/logging'

def deleteOutdatedLogs():
    global __logging_folder_path
    files = getAllLogFile()
    for key in files:
        if abs(key) > LIMIT_LOGGER:
            file_path = os.path.join(__logging_folder_path, files[key])
            os.remove(file_path)
            logging.info(f"Deleted outdated log file: {files[key]}")

def getAllLogFile()->Dict[int, str]:
    current_date = datetime.now()
    global __logging_folder_path
    files = os.listdir(__logging_folder_path)
    file_with_date = {}
    for file in files:
        if file.endswith('.log') and file.count('_') == 2:
            date_str = file.split('.')[0]
            try:
                file_date = datetime.strptime(date_str, '%y_%m_%d')
                days_difference = (current_date - file_date).days
                file_with_date[days_difference] = file
            except ValueError:
                # Handle cases where the date cannot be parsed
                logging.error(f"Ignored invalid log file name: {file}")
    return file_with_date

def downloadFile(filename: str):
    file_path = os.path.join(__logging_folder_path, filename)
    logging.error(filename)
    return send_file(file_path, as_attachment=True)