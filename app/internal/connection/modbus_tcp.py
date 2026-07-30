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
        'port': lambda value: isinstance(value, int) and value > 0,
        'unit_id': lambda value: value is None or (isinstance(value, int) and value >= 0)
    }

    def __init__(self) -> None:
        self.__temp = 0
        self._last_logged_registers = {}
        self._configure = {}
        super().__init__()

    def createConnection(self, config: dict)->bool:
        self.destroyConnection()
        self._configure = dict(config)
        self._configure['port'] = int(self._configure.get('port', 502))
        self._configure['unit_id'] = self._configure.get('unit_id') or 0
        try:
            self._connection = ModbusTcpClient(
                host=self._configure['ip'],
                port=self._configure['port']
            )
            if not self._connection.connect():
                self._closeConnection()
                logging.warning(
                    f"ModbusTCP connect failed ip={self._configure.get('ip')} "
                    f"port={self._configure.get('port')} unit_id={self._configure.get('unit_id')}"
                )
                return False
            else:
                logging.info(
                    f"ModbusTCP connect success ip={self._configure.get('ip')} "
                    f"port={self._configure.get('port')} unit_id={self._configure.get('unit_id')}"
                )
                return True
        except Exception as e:
            self._closeConnection()
            logging.error(
                f"ModbusTCP connect error ip={self._configure.get('ip')} "
                f"port={self._configure.get('port')} unit_id={self._configure.get('unit_id')}: {e}"
            )
            return False

    def _closeConnection(self):
        if self._connection != None:
            try:
                self._connection.close()
            except Exception as e:
                logging.warning(f"ModbusTCP close connection error: {e}")
            finally:
                self._connection = None

    def destroyConnection(self):
        self._closeConnection()

    def _read_holding_registers(self, start: int, length: int):
        unit_id = self._configure.get('unit_id') or 0
        return self._connection.read_holding_registers(start, length, unit=unit_id)

    def _write_registers(self, start: int, data: List[int]):
        unit_id = self._configure.get('unit_id') or 0
        return self._connection.write_registers(start, data, unit=unit_id)
        
    def _read(self, start: int, length: int, config: dict)->Optional[List[int]]:
        if self._connection == None:
            logging.warning("ModbusTCP read skipped because connection is not available")
            return None
        try:
            data = self._read_holding_registers(start, length)
            if data == None or (hasattr(data, 'isError') and data.isError()):
                logging.warning(
                    f"ModbusTCP read failed ip={self._configure.get('ip')} "
                    f"port={self._configure.get('port')} unit_id={self._configure.get('unit_id')} "
                    f"start={start} length={length} response={data}"
                )
                self._closeConnection()
                return None
            if not hasattr(data, 'registers'):
                logging.warning(
                    f"ModbusTCP read invalid response ip={self._configure.get('ip')} "
                    f"start={start} length={length} response={data}"
                )
                self._closeConnection()
                return None

            registers = data.registers
            block_key = (start, length)
            if self._last_logged_registers.get(block_key) != registers:
                logging.info(
                    f"ModbusTCP read ip={self._configure.get('ip')} "
                    f"start={start} length={length} registers={registers}"
                )
                self._last_logged_registers[block_key] = registers.copy()
            return registers
        except Exception as e:
            logging.error(
                f"ModbusTCP read error ip={self._configure.get('ip')} "
                f"port={self._configure.get('port')} unit_id={self._configure.get('unit_id')} "
                f"start={start} length={length}: {e}"
            )
            self._closeConnection()
            return None
        
    def _write(self, start: int, data: List[int], config: dict)->bool:
        if self._connection == None:
            logging.warning("ModbusTCP write skipped because connection is not available")
            return False
        try:
            result = self._write_registers(start, data)
            if result == None or (hasattr(result, 'isError') and result.isError()):
                logging.warning(
                    f"ModbusTCP write failed ip={self._configure.get('ip')} "
                    f"port={self._configure.get('port')} unit_id={self._configure.get('unit_id')} "
                    f"start={start} data={data} response={result}"
                )
                self._closeConnection()
                return False
        except Exception as e:
            logging.error(
                f"ModbusTCP write error ip={self._configure.get('ip')} "
                f"port={self._configure.get('port')} unit_id={self._configure.get('unit_id')} "
                f"start={start} data={data}: {e}"
            )
            self._closeConnection()
            return False
        return isinstance(result, SUCCESS)
