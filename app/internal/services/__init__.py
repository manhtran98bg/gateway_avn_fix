from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Dict, Type
import logging, threading
from abc import ABC, abstractmethod

executor = ThreadPoolExecutor(50)
__tasks: Dict[str, 'BaseService'] = {}
def assignTask(task_name: str, desc: str, *args: tuple, **kwargs: dict)->Callable:
    logging.info(f"Assign Task: {task_name}. Description: {desc}")
    def decorator(base_class: 'BaseService'):
        try:
            __tasks[task_name] = base_class(*args, **kwargs)
        except Exception as e:
            logging.error(e)
        return base_class
    return decorator

class BaseService(ABC):

    def __init__(self) -> None:
        self.mutex = threading.Lock()
        self.stop_notification = threading.Condition(self.mutex)
        self.keep_run = False

    @abstractmethod
    def _loop(self):
        pass

    def start(self):
        self.keep_run = True
        self._loop()

    def stop(self):
        self.keep_run = False
        with self.stop_notification:
            self.stop_notification.notify_all()

    def wait(self, timeout: float):
        with self.mutex:
            self.stop_notification.wait(timeout)

from .call_home import CallHomeProcess
from .mqtt_loop import MqttProcess, getMQTTConnectStatus, mqtt_internal_mutex
from .call_box_sync import CallBoxErrorService
from .oee_sync import SyncOEEData, SyncOEEDownTimeData, SyncOEEProductionData
from .clear_log import DeleteLogService
device_list = {}

def runExecutorMap():
    global __tasks
    try:
        executor.map(lambda task_name: __tasks[task_name].start(), __tasks.keys())
    except Exception as e:
        logging.error(e)

def stopAllTask():
    for task in __tasks:
        __tasks[task].stop()