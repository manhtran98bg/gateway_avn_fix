from flask import Flask
from flask_cors import CORS
import logging, os

#set up PATH to APP
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'app')
app = Flask(__name__, template_folder=TEMPLATE_PATH)
CORS(app, supports_credentials=True, expose_headers='*')
#Load config from YAML

from .internal.yaml_loader import (SOFTWARE_VER, AUTHOR, EMAIL,
                                LOGGING_LEVEL, DATABASE_URL, API_VERSION,
                                REDIS_HOST, REDIS_PORT, REDIS_PWD)

PREFIX = f'/api/{API_VERSION}'
logging.info("Start Rostek Gateway!!!!!!!!")
logging.info(f"+ Software version: {SOFTWARE_VER.upper()}")
logging.info(f"+ Logging: {LOGGING_LEVEL.upper()}")

from redis import Redis

redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PWD,
    charset="utf-8",
    decode_responses = True
)

#Load database
from app.models.databases import db
#load device list
from .internal.device import MonitorDevice
#load all api namespace
from app.dependencies.error_response import login_required, auth_header
from app.routers import api
#load protocol using serial
from .dependencies.com_manager import ComData
#load service
from app.internal.services import runExecutorMap, stopAllTask
#run service
runExecutorMap()
#run monitoring device
from app.internal.device import startDevice, stopDevice
startDevice()
import atexit
from app import stopAllTask

atexit.register(stopAllTask)
atexit.register(stopDevice)