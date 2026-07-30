from typing import List, Optional
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_write_message import WriteMultipleRegistersResponse as SUCCESS
import logging
from app.internal.yaml_loader import COM_DICT
from ..serial_com import parity_bit_type, byte_len_list, stop_bit_list
from app.dependencies.com_manager import SerialProtocol
from app.dependencies.device_config_format import DeviceConfigFormat

modbus_config_required = {
    'baudrate': lambda value: isinstance(value, int) and value > 0,
    'parity_bit': lambda value: isinstance(value, str) and value in parity_bit_type,
    'byte_len': lambda value: isinstance(value, int) and value in byte_len_list,
    'stop_bit_len': lambda value: isinstance(value, int) and value in stop_bit_list,
    'unit_id': lambda value: isinstance(value, int) and value > 0 and value < 254,
    'timeout': lambda value: float(value) > 0.,
    'com': lambda value: value in COM_DICT
}

def readModbus(start:int, length: int, config: DeviceConfigFormat, port: str, method: str)->Optional[List[int]]:
    protocol = config.protocol_config
    baudrate = protocol['baudrate']
    parity_bit = protocol['parity_bit']
    stop_bit_len = protocol['stop_bit_len']
    byte_len = protocol['byte_len']
    unit_id = protocol['unit_id']
    timeout = protocol['timeout']
    client = ModbusClient(method=method, port=port, baudrate=baudrate, timeout=timeout,
                          stop_bit_len=stop_bit_len, bytesize=byte_len, parity_bit=parity_bit)
    client.connect()
    try:
        result = client.read_holding_registers(address=start, count=length, unit=unit_id)
        r = None
        r = result.registers
    except Exception as e:
        logging.error(e)
    client.close()
    return r

def writeModbus(start:int, data: List[int], config: DeviceConfigFormat, port: str, method: str)->bool:
    protocol = config.protocol_config
    baudrate = protocol['baudrate']
    parity_bit = protocol['parity_bit']
    stop_bit_len = protocol['stop_bit_len']
    byte_len = protocol['byte_len']
    unit_id = protocol['unit_id']
    timeout = protocol['timeout']
    client = ModbusClient(method=method, port=port, baudrate=baudrate, timeout=timeout,
                          stop_bit_len=stop_bit_len, bytesize=byte_len, parity_bit=parity_bit)
    client.connect()
    try:
        result = client.write_registers(address=start, values=data, unit=unit_id)
    except Exception as e:
        logging.error(e)
        result = None
    client.close()
    return isinstance(result, SUCCESS)

from app.dependencies.com_manager import ComData

@ComData.assignSerialProtocol('modbus_rtu', 'Modbus RTU protocol', modbus_config_required)
class ModbusRTU(SerialProtocol):

    @staticmethod
    def _read(start: int, length: int, config: DeviceConfigFormat, port: str) -> Optional[List[int]]:
        return readModbus(start, length, config, port, 'rtu')
    
    @staticmethod
    def _write(start: int, data: List[int], config: DeviceConfigFormat, port: str)->bool:
        return writeModbus(start, data, config, port, 'rtu')
    
@ComData.assignSerialProtocol('modbus_ascii', 'Modbus ASCII protocol', modbus_config_required)
class ModbusASCII(SerialProtocol):

    @staticmethod
    def _read(start: int, length: int, config: DeviceConfigFormat, port: str) -> Optional[List[int]]:
        return readModbus(start, length, config, port, 'ascii')
    
    @staticmethod
    def _write(start: int, data: List[int], config: DeviceConfigFormat, port: str)->bool:
        return writeModbus(start, data, config, port, 'ascii')