from ..connection import MonitorConnection, TCPInterface
from typing import Union, List, Dict, Callable, Optional
from pymcprotocol import Type3E, Type4E
import logging

def createInstanceFromType(plc_series: str)->Union[Type3E ,Type4E ,None]:
    if plc_series == "Q":
        return Type3E()
    elif plc_series in ["L", "QnA", "iQ-L", "iQ-R"]:
        return Type3E(plctype=plc_series)
    elif plc_series == "4E":
        return Type4E()

@MonitorConnection.registerProtocol('mc_protocol', 'MC protocol over TCP/IP')
class MCProtocol(TCPInterface):
    protocol_name: str = ''
    _connection: Union[Type3E ,Type4E ,None] = None
    config_required: Dict[str, Callable] = {
        'ip': lambda value: isinstance(value, str),
        'port': lambda value: isinstance(value, int) and value > 0,
        'plc_series': lambda value: createInstanceFromType(value) != None,
        'comm_type': lambda value: value in ['binary', 'ascii']
    }
    def __init__(self) -> None:
        super().__init__()

    def createConnection(self, config: dict)->bool:
        self._configure = config
        try:
            self._connection = createInstanceFromType(self._configure['plc_series'])
            if self._configure['comm_type'] != 'ascii':
                self._connection.setaccessopt(commtype=self._configure['comm_type'])
            else:
                self._connection.setaccessopt()
            self._connection.connect(self._configure['ip'], self._configure['port'])
            return True
        except Exception as e:
            self._connection = None
            logging.error(str(e))
            return False
        
    def destroyConnection(self):
        if self._connection:
            self._connection.close()
            self._connection = None
        
    def _read(self, start: int, length: int, config: dict)->Optional[List[int]]:
        try:
            data = self._connection.batchread_wordunits(f'D{start}', length)
            return data
        except Exception as e:
            logging.error(str(e))
            self.destroyConnection()
            return None
        
    def _write(self, start: int, data: List[int], config: dict)->bool:
        try:
            self._connection.batchwrite_wordunits(f'D{start}', data)
            return True
        except Exception as e:
            logging.error(str(e))
            return False