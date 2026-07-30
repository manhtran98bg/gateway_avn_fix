from ..connection import MonitorConnection, TCPInterface
from typing import List, Dict, Callable, Optional
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_write_message import WriteMultipleRegistersResponse as SUCCESS
import logging
@MonitorConnection.registerProtocol('modbus_tcp', 'Modbus Over TCP/IP')
class ModbusTCP(TCPInterface):
    protocol_name: str = ''
    _connection: Optional[ModbusTcpClient] = None
    config_required: Dict[str, Callable] = {
        'ip': lambda value: isinstance(value, str),
        'port': lambda value: isinstance(value, int) and value > 0
    }
    def __init__(self) -> None:
        self.__temp = 0
        self._last_logged_registers = {}
        super().__init__()

    def createConnection(self, config: dict)->bool:
        self._configure = config
        self._configure['port'] = "502"
        try:
            self._connection = ModbusTcpClient(
                host=self._configure['ip'],
                port=self._configure['port']
            )
            if not self._connection.connect():
                self._connection.close() 
                self._connection = None
                logging.warning("Connect device failed")
                return False
            else:
                return True
        except Exception as e:
            self._connection = None
            logging.error(str(e))
            return False
        
    def destroyConnection(self):
        if self._connection != None:
            self._connection.close() 
            self._connection = None
        
    def _read(self, start: int, length: int, config: dict)->Optional[List[int]]:
        try:
            data = self._connection.read_holding_registers(start, length)
            if hasattr(data, 'registers'):
                registers = data.registers
                block_key = (start, length)
                if self._last_logged_registers.get(block_key) != registers:
                    logging.info(
                        f"ModbusTCP read ip={self._configure.get('ip')} "
                        f"start={start} length={length} registers={registers}"
                    )
                    self._last_logged_registers[block_key] = registers.copy()
                return data.registers
        except Exception as e:
            logging.error(str(e))
            self._connection.close()
            self._connection = None
            return None
        
    def _write(self, start: int, data: List[int], config: dict)->bool:
        try:
            result = self._connection.write_registers(start, data)
        except Exception as e:
            logging.error(str(e))
            result = None
        return isinstance(result, SUCCESS)
