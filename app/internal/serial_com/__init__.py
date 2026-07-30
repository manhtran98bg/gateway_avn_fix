parity_bit_type = ['odd', 'even', 'none']
byte_len_list = [7, 8]
stop_bit_list = [0, 1, 2]
from .modbus_serial import (ModbusRTU, ModbusASCII)
readSerial = (ModbusRTU, ModbusASCII)