from ..connection import MonitorConnection
from app.dependencies.com_manager import ComData
from typing import Dict, Callable, List, Optional
import logging
from app.dependencies.com_manager import ComData
from app.internal.serial_com import readSerial
from app.dependencies.register_format import RegisterFormat

@MonitorConnection.registerProtocol([serial for serial in ComData.protocol_list], 
                                       'All protocol run in Serial Port')
class SerialConnection(MonitorConnection):
    protocol_name: str = ''
    com: Optional[ComData] = None
    def __init__(self) -> None:
        super().__init__()
    def get_static_variable(self)->Dict[str, Callable]:
        if self.protocol_name in ComData.protocol_list:
            return ComData.config_required[self.protocol_name]
        return {}
    config_required = property(get_static_variable)

    def createConnection(self, config: dict)->bool:
        com = config.get('com')
        if com in ComData.com_list and self.protocol_name in ComData.protocol_list:
            self.com = ComData.com_list[com]
            return True
        return False

    def readData(self,config: dict, monitor_func: Callable[[],bool])->Optional[List[RegisterFormat]]:
        if self.com != None:
            return self.com.readRegister(config, self.protocol_name, monitor_func)
        
    def writeData(self,config: dict, write_data: List[RegisterFormat],
                monitor_func: Callable[[],bool])->bool:
        if self.com != None:
            return self.com.writeRegister(config,
                self.protocol_name, write_data, monitor_func)
        
    def destroyConnection(self):
        logging.debug('Close Serial Communication')