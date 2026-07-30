from dataclasses import dataclass, field
from queue import Queue
from app.internal.yaml_loader import COM_DICT
from typing import Callable, Dict, Type, List, Optional
import logging
import threading
from abc import ABC, abstractmethod
from app.dependencies.register import readRegister, writeRegister
from app.dependencies.register_format import RegisterFormat

class SerialProtocol(ABC):

    @classmethod
    @readRegister
    def read(cls, start: int, length: int, config: dict, port: str)->Optional[List[RegisterFormat]]:
        return cls._read(start, length, config, port)
    
    @classmethod
    @writeRegister
    def write(cls, start: int, data: List[int], config: dict, port: str)->bool:
        return cls._write(start, data, config, port)

    @staticmethod
    @abstractmethod
    def _read(start: int, length: int, config: dict, port: str)->Optional[List[RegisterFormat]]:
        pass

    @staticmethod
    @abstractmethod
    def _write(start: int, data: List[int], config: dict, port: str)->bool:
        pass

@dataclass
class ComData(object):
    name: str
    port: str
    command_queue: Queue = Queue(100)
    mutex: threading.Lock = threading.Lock()

    com_list: Dict[str, 'ComData'] = field(default=None)
    protocol_list: Dict[str, Type['SerialProtocol']] = field(default=None)
    config_required: Dict[str, list] = field(default=None)

    def readRegister(self, config: dict, protocol: str, 
                     monitor_func: Callable[[],bool])->Optional[RegisterFormat]:
        if protocol not in ComData.protocol_list:
            return None
        return ComData.protocol_list[protocol].read(config=config, 
            com=self, monitor_func=monitor_func)
    
    def writeRegister(self, config: dict, protocol: str, write_data: List[RegisterFormat],
                     monitor_func: Callable[[],bool])->bool:
        if protocol not in ComData.protocol_list:
            return False
        return ComData.protocol_list[protocol].write(config=config, 
            com=self, monitor_func=monitor_func, write_data=write_data)

    @staticmethod
    def assignSerialProtocol(protocol: str, description: str,
            config_required: Dict[str, Type['SerialProtocol']])->Type['SerialProtocol']:
        logging.info(f'Add protocol {protocol}. Description: {description}')
        if ComData.protocol_list == None:
            ComData.protocol_list = {}
        if ComData.config_required == None:
            ComData.config_required = {}
        def decorator(cls: Type['SerialProtocol']):
            ComData.protocol_list[protocol] = cls
            ComData.config_required[protocol] = config_required
            return cls
        return decorator

    @classmethod
    def loadComConfig(cls: 'ComData', config: dict):
        ComData.com_list = {}
        for key in config:
            ComData.com_list[key] = cls(key, config[key])

ComData.loadComConfig(COM_DICT)