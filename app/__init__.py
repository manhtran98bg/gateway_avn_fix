from flask import Flask
from flask_cors import CORS
import logging, os, threading
from time import sleep

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
from redis.exceptions import RedisError

class ReconnectingRedis:
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._lock = threading.Lock()
        self._client = self._create_client()

    def _create_client(self):
        return Redis(**self._kwargs)

    def _reconnect(self):
        with self._lock:
            try:
                self._client.connection_pool.disconnect()
            except Exception as e:
                logging.warning(f"Redis disconnect before reconnect failed: {e}")
            self._client = self._create_client()

    def __getattr__(self, name):
        attr = getattr(self._client, name)
        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(2):
                try:
                    return getattr(self._client, name)(*args, **kwargs)
                except (RedisError, OSError) as e:
                    last_error = e
                    logging.warning(f"Redis command {name} failed. Reconnect attempt {attempt + 1}: {e}")
                    self._reconnect()
                    sleep(0.2)
            raise last_error
        return wrapper

redis_client = ReconnectingRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PWD,
    encoding="utf-8",
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
    retry_on_timeout=True
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
