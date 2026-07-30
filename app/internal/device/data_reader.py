from . import MonitorDevice
from app.dependencies.type_define import DeviceTypes
from typing import List, Dict, Tuple, Optional, Type, Union
import logging, time
from app.dependencies.mqtt_utils import MqttTopic
from app.dependencies.register_format import RegisterFormat
from dataclasses import dataclass

def bitCheck(bit: Optional[int])->bool:
    if bit == None:
        return True
    elif bit > 15 and bit < 0:
        return False
    else:
        return True

def dataInputCheck(values: List[dict])->bool:
    if len(values) == 0:
        return False
    keys = []
    for value in values:
        name = value["name"]
        index = int(value["index"])
        bit = int(value["bit"]) if value["bit"] != None else None
        if (name in keys or name == "" or not 
            isinstance(name, str) or index < 0 
            or not bitCheck(bit)):
            return False
    return True

def getBitAtIndex(number: int, index: int):
    # Check if the index is valid
    if index < 0 or index >= 16:
        raise ValueError("Index must be between 0 and 15 for a 16-bit integer")

    # Use bitwise operations to get the bit value at the specified index
    bit_value = (number >> index) & 1
    return bit_value

@dataclass
class MonitorFormat:
    index: int
    bit: Optional[int]

@MonitorDevice.registerDevice(DeviceTypes.DATA_READER.value, "Class for data reader")
class DataReader(MonitorDevice):
    register_required: List[str] = ['start_address']
    device_configuration: Dict[str, callable] = {
        'mqtt_topic': lambda value: isinstance(value, str) and len(value) > 0,
        'scan_interval': lambda value: float(value) > 0,
        'data_input': lambda value: dataInputCheck(value)
    }

    def __init__(self, configure: dict, protocol: str):
        super().__init__(configure, protocol)
        self._map_data: Dict[str, MonitorFormat] = {}
        data_input = self.device["data_input"]
        extent_register: List[RegisterFormat] = []
        start_index = self.registers[0].address
        for data in data_input:
            name = data["name"]
            index = int(data["index"])
            bit = int(data["bit"]) if data["bit"] != None else None
            self._map_data[name] = MonitorFormat(index, bit)
            extent_register.append(RegisterFormat(name, index+start_index))
        self.read_registers.extend(extent_register)
        self.topic = self.device["mqtt_topic"]


    @classmethod
    def updateRequired(cls: Type['DataReader'], device: Dict[str, any],
            registers: List[str])->Tuple[Dict[str, any], List[str]]:
        return cls.device_configuration, registers
    
    def _readDeviceData(self)->bool:
        registers = self._readPLCRegister()
        return_value = False
        try:
            if registers != None:
                payload = self._readRegisterSuccess(registers)
                return_value = True
            else:
                payload = self._readRegisterFailed()
                return_value = False
            MqttTopic.putToQueue(self.topic, payload)
        except Exception as e:
            logging.error(e)
        return return_value
    
    def _readRegisterSuccess(self,
            registers: List[RegisterFormat])->Dict[str, Union[None, int, bool]]:
        payload = {}
        for register in registers:
            name = register.name
            bit_index = self._map_data[name].bit
            value = register.value
            if bit_index == None:
                payload[name] = value
            else:
                payload[name] = getBitAtIndex(value, bit_index)
        return payload

    def _readRegisterFailed(self)->Dict[str, Union[None, int, bool]]:
        payload = {
            name: None
            for name in self._map_data
        }
        return payload
    
    def _getRedisData(self):
        logging.debug('No data cache')
    
    def cloudSyncChangeProduct(self, payload: dict):
        logging.debug(f'No sync: {payload}')

    def cloudSyncMachine(self, payload: dict):
        logging.debug(f'No sync: {payload}')

    def cloudSyncDowntime(self, payload: dict):
        logging.debug(f'No sync: {payload}')

    def cloudCmdHandle(self, payload: dict):
        logging.debug(f'No cmd: {payload}')

    def cloudSettings(self, payload: dict):
        logging.debug(f'No setting: {payload}')

    def clearDataStorage(self, no_commit: bool = False):
        logging.debug('No clear')

    def getStatus(self)->dict:
        return self.last_read

    def controlOverAPI(self, cmd: dict)->Tuple[bool, str]:
        logging.debug('No control')