from enum import Enum
from typing import Optional
import logging

def convertKeyToEnum(device: any, ref: Enum)->Optional[any]:
    try:
        return ref[ref(device).name]
    except Exception as e:
        logging.error(e)
        return None

class DeviceTypes(Enum):
    OEE = 'oee'
    CALL_BOX = 'call_box'
    STATUS_MONITORING = 'status_monitoring'
    PLC_MONITOR = 'pcl_monitor'
    DATA_READER = 'data_reader'
    MEASURE = 'measure'

class GeneralLogType(Enum):
    NETWORK = 'network'
    MQTT = 'mqtt'
        
class LogModule(Enum):
    NETWORK = "network"
    MQTT = "mqtt"
    DEVICE = "device"
    SYSTEM = "system"

class WorkStatus(Enum):
    SUCCESS = 200
    ERROR = 402

class LogType(Enum):
    UPDATE = "update"
    ERROR = "error"
    INFO = "info"
    DELETE = "delete"
    ADD_DEVICE = 'add_device'

class STATUS(Enum):
    DISCONNECT = 0
    RUN = 1
    IDLE = 2
    ERROR = 3

class MqttInternalTopic(Enum):
    UPDATE = 'update'
    SUB = 'sub'
    UNSUB = 'unsub'

class ErrorCode(Enum):
    DISCONNECTED = 1400
    CAN_NOT_CALL_SERVER = 1401