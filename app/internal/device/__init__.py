from abc import ABC, abstractmethod
import logging, threading
from app.models.databases.gateway_db import Device, DeviceGroup
from typing import Type, Dict, List, Tuple, Optional
from ..connection import MonitorConnection
from app import db
from time import time
from app.dependencies.register_format import RegisterFormat
from app.dependencies.device_config_format import DeviceConfigFormat

class MonitorDevice(ABC):
    operator_device_list: Dict[str, 'MonitorDevice'] = {} # list of running device
    device_type_list: Dict[str, Type['MonitorDevice']] = {} # list of available device
    device_type: str = '' # device type of instance
    device_args_required = ['registers', 'type', 'protocol', 'protocol_type', 'device'] # list of data need to be provided
    register_required: List[str] = [] # list register need to be provide to read data
    device_configuration: Dict[str, callable] = {} # List of configuration and checking function

    @staticmethod
    def registerDevice(name: str, description: str)->callable:
        def decorator(cls):
            logging.info(f'Register new device type: {name}. Description: {description}')
            MonitorDevice.device_type_list[name] = cls
            return cls
        return decorator
    
    @classmethod
    @abstractmethod
    def updateRequired(cls: Type['MonitorDevice'], device: Dict[str, any],
            registers: List[str])->Tuple[Dict[str, callable], List[str]]:
        return cls.device_configuration, registers

    def __init__(self,configure: dict, protocol: str):
        self._configure: DeviceConfigFormat = DeviceConfigFormat.dictToDeviceConfig(configure, protocol)
        self._id: str = configure['device_id']
        self._protocol: str = protocol
        self._is_connected = False
        self._monitoring = False
        self._setup()
        self._getRedisData()
        self.wait_mutex = threading.Lock()
        self.waiting = threading.Condition(self.wait_mutex)
        self._last_read_status = False
        self._connect_failed_cnt = 0

    @property
    def device(self)->Dict[str, any]:
        return self._configure.device_config
    
    @property
    def protocol(self)->Dict[str, any]:
        return self._configure.protocol_config
    
    @property
    def registers(self)->List[RegisterFormat]:
        return self._configure.registers
    
    @property
    def write_registers(self)->List[RegisterFormat]:
        return self._configure.write_registers
    
    @property
    def read_registers(self)->List[RegisterFormat]:
        return self._configure.read_registers

    def __hash__(self):
        return self._id.__hash__()
    
    def __str__(self):
        return self._id

    def wait(self, timeout: float, start_wait: Optional[float] = None):
        if start_wait != None:
            working_time = time() - start_wait
            if working_time >= timeout:
                return
            else:
                timeout = timeout - working_time
        self.waiting.wait(timeout)

    def _setup(self):
        self._connection = MonitorConnection.createMonitorConnect(self._protocol)
        self.scan_interval = self.device.get('scan_interval', 1.0)

    def _connectPLC(self):
        if self._connection != None:
            self._is_connected = self._connection.createConnection(self.protocol)
        if not self._is_connected:
            self.wait(10.0)
    
    def _disconnectPLC(self):
        if self._connection != None:
            self._connection.destroyConnection()
            self._is_connected = False
    
    def _readPLCRegister(self) -> Optional[List[RegisterFormat]]:
        if self._connection != None:
            return self._connection.readData(self._configure, self._is_monitoring)
        
    def _writePLCRegister(self, write_data: List[RegisterFormat]) -> bool:
        if self._connection != None and write_data:
            return self._connection.writeData(self._configure, write_data, self._is_monitoring)
        return False
    
    def connectStatus(self)->bool:
        return self._is_connected and self._last_read_status

    def _startReadingPLC(self):
        self._connect_failed_cnt = 0
        while self._monitoring:
            start_loop = time()
            try:
                with self.wait_mutex:
                    if not self._is_connected:
                        self._last_read_status = False
                        self._connectPLC()
                    elif not self._readDeviceData():
                        self._last_read_status = False
                        self._connect_failed_cnt += 1
                        logging.warning(f"Read PLC failed. Reconnect device {self._id}")
                        self._disconnectPLC()
                        self.wait(5.0, start_loop)
                        # print("READ FAIL", self._id)
                    else:
                        self._connect_failed_cnt = 0
                        self._last_read_status = True
                        self.wait(self.scan_interval, start_loop)
            except Exception as e:
                self._last_read_status = False
                self._connect_failed_cnt += 1
                logging.error(e)
                self._disconnectPLC()
                self.wait(5.0, start_loop)
            if self._connect_failed_cnt == 3:
                # print("READ TIMEOUT. Reconnect", self._id)
                self._connect_failed_cnt = 0
                self._last_read_status = False
                self._is_connected = False

    def _is_monitoring(self):
        return self._monitoring
    
    @abstractmethod
    def _readDeviceData(self)->bool:
        return False
    
    @abstractmethod
    def _getRedisData(self):
        return
    
    @abstractmethod
    def cloudSyncChangeProduct(self, payload: dict):
        pass

    @abstractmethod
    def cloudSyncMachine(self, payload: dict):
        pass

    @abstractmethod
    def cloudSyncDowntime(self, payload: dict):
        pass

    @abstractmethod
    def cloudCmdHandle(self, payload: dict):
        pass

    @abstractmethod
    def cloudSettings(self, payload: dict):
        pass

    @abstractmethod
    def clearDataStorage(self, no_commit: bool = False):
        pass

    @abstractmethod
    def getStatus(self)->dict:
        pass

    @abstractmethod
    def controlOverAPI(self, cmd: dict)->Tuple[bool, str]:
        pass
    
    def start(self):
        self._monitoring = True
        logging.info("Start monitoring successful")
        self._startReadingPLC()

    def stop(self):
        self._monitoring = False
        with self.wait_mutex:
            self.waiting.notify()
            logging.info("Stop monitoring successful")
            self._disconnectPLC()

    def update(self, configure: dict, protocol: str):
        with self.wait_mutex:
            self._configure = configure
            self._protocol = protocol
            if self._connection != None:
                self._connection.destroyConnection()
                self._is_connected = False
            self._setup()

    def __del__(self):
        logging.info(f"Delete Device with id {self._id}")

from app.internal.services import executor

from .device_utils import (postToDB, postPreCheck, createDeviceByID,
        putToDB, startMonitor, stopMonitor, stopDevice, startDevice)
from .oee_device import OEEDevice
from .callbox_device import CallBoxDevice
from .plc_monitor import StatusMonitoring
from .data_reader import DataReader
from .measure import Measure
