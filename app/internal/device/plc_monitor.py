from . import MonitorDevice
from app.dependencies.type_define import DeviceTypes
from typing import List, Dict, Tuple, Optional, Type
import logging, time
from app.dependencies.mqtt_utils import MqttTopic
from app.dependencies.register_format import RegisterFormat

@MonitorDevice.registerDevice(DeviceTypes.PLC_MONITOR.value, "Class for PLC monitor")
class StatusMonitoring(MonitorDevice):
    register_required: List[str] = ['status', 'errors', 'inputs', 'outputs', 'analogs']
    device_configuration: Dict[str, callable] = {
        'max_retry': lambda value: int(value) > 0,
        'total_errors': lambda value: int(value) > 0,
        'total_inputs': lambda value: int(value) > 0,
        'total_outputs': lambda value: int(value) > 0,
        'total_analogs': lambda value: int(value) > 0,
        'scan_interval': lambda value: int(value) > 0,
        'start_input': lambda value: int(value) >= 0,
        'start_output': lambda value: int(value) >= 0,
        'start_analog': lambda value: int(value) >= 0
    }
    machine_status = {
        1: "Fault",
        2: "EMC",
        4: "No Cycle Started",
        8: "Manual",
        16: "Production Stop",
        32: "Starved",
        64: "No Material",
        128: "Blocked",
        256: "Tool Change",
        512: "Quality Alert",
        1024: "Quality Check",
        2048: "Production"
    }

    def __init__(self, configure: dict, protocol: str):
        super().__init__(configure, protocol)
        self.last_read = {}
        errors = int(self.device['total_errors'])
        inputs = int(self.device['total_inputs'])
        outputs = int(self.device['total_outputs'])
        analogs = int(self.device['total_analogs'])
        extent_register: List[RegisterFormat] = []
        registers = {
            register.name: register.address
            for register in self.registers
        }
        for i in range(1, errors):
            extent_register.append(RegisterFormat(
                name='errors{i}',
                address=i + registers['errors']
            ))
        for i in range(1, inputs):
            extent_register.append(RegisterFormat(
                name='inputs{i}',
                address=i + registers['inputs']
            ))
        for i in range(1, outputs):
            extent_register.append(RegisterFormat(
                name='outputs{i}',
                address=i + registers['outputs']
            ))
        for i in range(1, analogs):
            extent_register.append(RegisterFormat(
                name='analogs{i}',
                address=i + registers['analogs']
            ))
        self.read_registers.extend(extent_register)

    @classmethod
    def updateRequired(cls: Type['StatusMonitoring'], device: Dict[str, any],
            registers: List[str])->Tuple[Dict[str, any], List[str]]:
        return cls.device_configuration, registers
        
    def _getMachineStatus(self, status: Optional[int]):
        return StatusMonitoring.machine_status.get(status, "Fault")
    
    def _getErrorsList(self, error_list: Dict[str, int])->List[int]:
        result = []
        for key in error_list:
            num = error_list[key]
            name = key
            if name != 'errors':
                i = int(name[6:])
            else:
                i = 0
            for bit_index in range(16):
                if (num >> bit_index) & 1:
                    result.append(i * 20 + bit_index + 1)
        return result
    
    def _getInputsList(self, inputs: Dict[str, int])->Dict[str, bool]:
        result = {}
        start_input = int(self.device['start_input'])
        for key in inputs:
            num = inputs[key]
            name = key
            if name != 'inputs':
                i = int(name[6:])
            else:
                i = 0
            for bit_index in range(8):
                value = (num >> bit_index) & 1
                result[f'x{start_input+2*i}{bit_index}'] = bool(value)
            for bit_index in range(8, 16):
                value = (num >> bit_index) & 1
                result[f'x{start_input+2*i+1}{bit_index-8}'] = bool(value)
        return result

    def _getOutputsList(self, outputs: Dict[str, int])->Dict[str, bool]:
        result = {}
        start_output = int(self.device['start_output'])
        for key in outputs:
            num = outputs[key]
            name = key
            if name != 'outputs':
                i = int(name[7:])
            else:
                i = 0
            for bit_index in range(8):
                value = (num >> bit_index) & 1
                result[f'y{start_output+2*i}{bit_index}'] = bool(value)
            for bit_index in range(8, 16):
                value = (num >> bit_index) & 1
                result[f'y{start_output+2*i+1}{bit_index-8}'] = bool(value)
        return result

    def _getAnalogsList(self, analogs: Dict[str, int])->Dict[str, int]:
        result = {}
        start_analog = int(self.device['start_analog'])
        for key in analogs:
            num = analogs[key]
            name = key
            if name != 'analogs':
                i = int(name[7:])
            else:
                i = 0
            result[f'a{start_analog+i}'] = num
        return result

    def _readDeviceData(self)->bool:
        self._max_reading_rate = 0.0
        start_time = time.time()
        values = self._readPLCRegister()
        errors = {}
        inputs = {}
        outputs = {}
        analogs = {}
        status = "Fault"
        if values != None:
            for value in values:
                name = value.name
                if 'inputs' in name:
                    inputs[name] = value.value
                elif 'outputs' in name:
                    outputs[name] = value.value
                elif 'errors' in name:
                    errors[name] = value.value
                elif 'analogs' in name:
                    analogs[name] = value.value
                elif name == 'status':
                    status = self._getMachineStatus(value.value)
            self.last_read = {
                'status': status,
                'errors': self._getErrorsList(errors),
                'input': self._getInputsList(inputs),
                'output': self._getOutputsList(outputs),
                'analog': self._getAnalogsList(analogs),
                'id': self._id,
            }
            logging.error(self.last_read)
            MqttTopic.putToQueue("machine_status", self.last_read)
            delta_time = time.time() - start_time
            wait = float(self.device['scan_interval']) - delta_time
            if wait > 0:
                self.wait(wait)
            return True
        else:
            payload = {
                'status': "Read Failed"
            }
            MqttTopic.putToQueue("machine_status", payload)
            return False
    
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