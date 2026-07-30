from ..connection import MonitorConnection, TCPInterface
from typing import List, Dict, Callable, Optional
from snap7.client import Client
import logging

@MonitorConnection.registerProtocol('s7_snap', 'Connection with Siemens')
class S7Snap(TCPInterface):
    protocol_name: str = ''
    config_required: Dict[str, Callable] = {
        'ip': lambda value: isinstance(value, str),
        'tcpport': lambda value: isinstance(value, int) and value > 0,
        'rack': lambda value: isinstance(value, int) and value > 0,
        'slot': lambda value: isinstance(value, int) and value >= 0,
        'db': lambda value: isinstance(value, int) and value > 0
    }
    _connection: Optional[Client] = None
    def __init__(self) -> None:
        super().__init__()

    def createConnection(self, config: dict)->bool:
        self._configure = config
        try:
            self._connection = Client()
            self._connection.connect(
                address=self._configure["ip"],
                rack=self._configure["rack"],
                slot=self._configure["slot"],
                tcpport=self._configure["tcpport"]
            )
            if self._connection.get_connected():
                return True
            else:
                self._connection = None
                return False
        except Exception as e:
            self._connection = None
            logging.error(str(e))
            return False

    def destroyConnection(self):
        if self._connection != None:
            self._connection = None
        
    def _read(self, start: int, length: int, config: dict)->Optional[List[int]]:
        try:
            data_bytes = self._connection.db_read(
                self._configure["db"], 
                start, 
                length*2)
            data = []
            for i in range(len(data_bytes)):
                value = int.from_bytes(data_bytes[2*i:2*i+2], "big")
                data.append(value)
            return data
        except Exception as e:
            logging.error(str(e))
            self._connection = None
            return None
        
    def _write(self, start: int, data: List[int], config: dict)->bool:
        value = b''
        for i in data:
            value += i.to_bytes(2, 'big')
            
        try:
            result = self._connection.db_write(self._configure["db"],
                    start, value)
            return result != 0
        except Exception as e:
            logging.error(e)
            return False