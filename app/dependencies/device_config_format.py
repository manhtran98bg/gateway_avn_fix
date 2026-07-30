from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from app.dependencies.register_format import RegisterFormat

@dataclass
class DeviceConfigFormat(object):
    protocol_name: str
    protocol_config: Dict[str, any]
    device_config: Dict[str, any]
    registers: List[RegisterFormat]
    read_registers: List[RegisterFormat] = field(default_factory=list)
    write_registers: List[RegisterFormat] = field(default_factory=list)
    scan_interval: float = 0.1

    def getProtocol(self)->Tuple[str, Dict[str, any]]:
        return self.protocol_name, self.protocol_config
    
    def getDevice(self)->Dict[str, any]:
        return self.device_config
    
    def getRegister(self)->List[Dict[str, int]]:
        return [{
            'name': register.name,
            'addr': register.address
        } for register in self.registers]

    @staticmethod
    def dictToDeviceConfig(config: Dict[str, any], protocol_name: str)->'DeviceConfigFormat':
        raw_registers = config.get('register', [])
        registers = RegisterFormat.listToListRegisters(raw_registers)
        return DeviceConfigFormat(
            protocol_name=protocol_name,
            protocol_config=config.get('protocol', {}),
            device_config=config.get('device', {}),
            registers=registers,
            scan_interval=config.get('device', {}).get('scan_interval', 0.1)
        )