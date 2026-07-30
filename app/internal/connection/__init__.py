from abc import ABC, abstractmethod
from typing import Union, Dict, Type, List, Callable, Optional
import logging
from app.dependencies.register import readRegister, writeRegister
from app.dependencies.register_format import RegisterFormat
from app.dependencies.device_config_format import DeviceConfigFormat

class MonitorConnection(ABC):
    protocol_name: str = ""
    protocol_list: Dict[str, Type['MonitorConnection']] = {}
    config_required: List[str] = []
    @staticmethod
    def registerProtocol(protocols: Union[str, List[str]], description: str):
        logging.info(f'Register protocol: {protocols}. Description: {description}')
        def decorator(cls):
            if isinstance(protocols, str):
                MonitorConnection.protocol_list[protocols] = cls
                cls.protocol_name = protocols
            elif isinstance(protocols, list):
                for protocol in protocols:
                    MonitorConnection.protocol_list[protocol] = cls
            return cls
        return decorator

    @staticmethod
    def createMonitorConnect(protocol: str)->Optional['MonitorConnection']:
        if protocol in MonitorConnection.protocol_list:
            connection = MonitorConnection.protocol_list[protocol]()
            connection.protocol_name = protocol
            return connection

    @abstractmethod
    def createConnection(self, config: Dict[str, any])->bool:
        return False

    @abstractmethod
    def destroyConnection(self):
        pass

    @abstractmethod
    def readData(self,config: DeviceConfigFormat, monitor_func: Callable[[],bool])->Optional[List[RegisterFormat]]:
        pass

    @abstractmethod
    def writeData(self,config: DeviceConfigFormat, write_data: List[RegisterFormat],
            monitor_func: Callable[[],bool])->bool:
        pass

class TCPInterface(MonitorConnection):
    def readData(self,config: dict, monitor_func: Callable[[],bool])->Optional[List[RegisterFormat]]:
        if self._connection != None:
            return self.read(config=config, monitor_func=monitor_func)
        
    def writeData(self,config: dict, write_data: List[RegisterFormat],
                monitor_func: Callable[[],bool])->bool:
        if self._connection != None:
            return self.write(config=config, monitor_func=monitor_func,
                        write_data=write_data)
        return False
    
    @readRegister
    def read(self, start: int, length: int, config: DeviceConfigFormat)->Optional[List[int]]:
        return self._read(start, length, config)
    
    @writeRegister
    def write(self, start: int, data: List[int], config: DeviceConfigFormat)->bool:
        return self._write(start, data, config)

    @abstractmethod
    def _read(self, start: int, length: int, config: DeviceConfigFormat)->Optional[List[int]]:
        pass
        
    @abstractmethod
    def _write(self, start: int, data: List[int], config: DeviceConfigFormat)->bool:
        pass

from .modbus_tcp import ModbusTCP
from .s7_snap import S7Snap
from .mc_protocol import MCProtocol
from .serial_connection import SerialConnection