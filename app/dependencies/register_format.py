from dataclasses import dataclass
from typing import List, Dict

@dataclass
class RegisterFormat(object):
    name: str
    address: int
    value: int = 0

    def __dict__(self)->Dict[str, int]:
        return {
            'name': self.name,
            'addr': self.address
        }
    
    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def __str__(self) -> str:
        return self.name

    @staticmethod
    def listToListRegisters(str_list: List[dict])->List['RegisterFormat']:
        return [RegisterFormat(
            name=value['name'],
            address=value['addr']
        ) for value in str_list]

    @staticmethod
    def listRegistersToList(registers: List['RegisterFormat'])->List[dict]:
        return [register.__dict__() for register in registers]
    
    @staticmethod
    def listToDictRegisters(registers: List[dict])->Dict[str, 'RegisterFormat']:
        return {
            register['name']: RegisterFormat(
                name=register['name'],
                address=register['addr']  
            )
            for register in registers
        }