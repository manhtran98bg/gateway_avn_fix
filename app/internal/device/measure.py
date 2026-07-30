from . import MonitorDevice
from app.dependencies.type_define import DeviceTypes
from typing import List, Dict, Tuple, Optional, Type, Union
import logging, time
from app.dependencies.mqtt_utils import MqttTopic
from app.dependencies.register_format import RegisterFormat
from dataclasses import dataclass

def valueCheck(bit: Optional[int])->bool:
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
        scale = int(value["scale"]) if value["scale"] != None else None
        offset = int(value["offset"]) if value["offset"] != None else None
        if (name in keys or name == "" or not 
            isinstance(name, str) or index < 0 
            or not valueCheck(scale) or not valueCheck(offset)):
            return False
    return True

@dataclass
class MeasureFormat:
    index: int
    scale: int
    offset: int

@MonitorDevice.registerDevice(DeviceTypes.MEASURE.value, "Class for data reader")
class Measure(MonitorDevice):
    register_required: List[str] = ['start_address']
    device_configuration: Dict[str, callable] = {
        'mqtt_topic': lambda value: isinstance(value, str) and len(value) > 0,
        'scan_interval': lambda value: float(value) > 0,
        'data_input': lambda value: dataInputCheck(value)
    }

    def __init__(self, configure: dict, protocol: str):
        super().__init__(configure, protocol)
        self._map_data: Dict[str, MeasureFormat] = {}
        data_input = self.device["data_input"]
        extent_register: List[RegisterFormat] = []
        start_index = self.registers[0].address
        for data in data_input:
            name = data["name"]
            index = int(data["index"])
            scale = int(data["scale"]) if data["scale"] != None else 1
            offset = int(data["offset"]) if data["offset"] != None else 1
            self._map_data[name] = MeasureFormat(index, scale, offset)
            extent_register.append(RegisterFormat(name, index+start_index))
        self.read_registers.extend(extent_register)
        self.topic = self.device["mqtt_topic"]


    @classmethod
    def updateRequired(cls: Type['Measure'], device: Dict[str, any],
            registers: List[str])->Tuple[Dict[str, any], List[str]]:
        return cls.device_configuration, registers
    
    def _readDeviceData(self)->bool:
        registers = self._readPLCRegister()
        return_value = False
        registers = None
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
            scale = self._map_data[name].scale
            offset = self._map_data[name].offset
            value = register.value
            payload[name] = value/scale - offset
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