from typing import Callable, List, Optional
from functools import wraps
import logging
from app.dependencies.register_format import RegisterFormat
from app.dependencies.device_config_format import DeviceConfigFormat

condition_split_read = lambda item, start_item: item['addr'] - start_item['addr'] <= 50
condition_split_write = lambda item, front_item: item['addr'] - front_item['addr'] <= 1

def conditionSplitRead(item: RegisterFormat, start_time: RegisterFormat):
    return (item.address - start_time.address) <= 50

def conditionSplitWrite(item: RegisterFormat, front_item: RegisterFormat):
    return (item.address - front_item.address) <= 1

def splitListByCondition(data: List[RegisterFormat], read_list: bool)-> List[List[RegisterFormat]]:
    subgroups: List[List[RegisterFormat]] = []
    current_group = [data[0]]
    condition = conditionSplitRead if read_list else conditionSplitWrite
    for i in range(1, len(data)):
        ref_register = current_group[0] if read_list else current_group[-1]
        if condition(data[i], ref_register):
            current_group.append(data[i])
        else:
            subgroups.append(current_group)
            current_group = [data[i]]
    subgroups.append(current_group)
    return subgroups

def createRegisterList(register_list: List[RegisterFormat], read_list: bool = True)->List[List[RegisterFormat]]:
    sort_list = sorted(register_list, key=lambda x: x.address)
    return splitListByCondition(sort_list, read_list)

def readBySerial(cls, com: 'ComData', start: int, length: int, 
              config: DeviceConfigFormat, func: Callable,
              monitor_func: Callable[[], bool])->Optional[List[int]]:
    retry = 0
    sub_register_group = None
    protocol = config.protocol_config
    max_retry = protocol['max_retry'] if 'max_retry' in protocol else 2
    with com.mutex:
        while (sub_register_group == None) and (retry < max_retry) and monitor_func():
            sub_register_group = func(cls, start, length, config, com.port)
            retry += 1
    return sub_register_group

def readByTCP(self: Optional[object], start: int, length: int, config: DeviceConfigFormat, 
              func: Callable, monitor_func: Callable[[], bool])->Optional[List[int]]:
    retry = 0
    sub_register_group = None
    protocol = config.protocol_config
    max_retry = protocol['max_retry'] if 'max_retry' in protocol else 2.
    try:
        while (sub_register_group == None) and (retry < max_retry) and monitor_func():
            if self != None:
                sub_register_group = func(self, start, length, config)
            else:
                sub_register_group = func(start, length, config)
            retry += 1
    except Exception as e:
        logging.error(e)
    return sub_register_group

def mappingReadData(ref: List[RegisterFormat], data: List[int])->List[RegisterFormat]:
    for reg in ref:
        index = reg.address - ref[0].address
        reg.value = data[index]
    return ref

def readRegister(func: Callable[[int, int, dict, Optional['ComData']],List[int]]):
    @wraps(func)
    def decorator(*args, **kwargs)->Optional[List[RegisterFormat]]:
        config: DeviceConfigFormat = kwargs.get('config')
        com: Optional[ComData] = kwargs.get('com')
        monitor_func: Callable[[], bool] = kwargs.get('monitor_func')
        registers = config.read_registers
        if len(args) == 1:
            self = args[0]
            cls = args[0]
        else:
            self = None
            cls = None
        subgroups = createRegisterList(registers)
        groups = []
        for sub in subgroups:
            length = sub[-1].address - sub[0].address + 1
            start = sub[0].address
            sub_register_group = None
            if not monitor_func():
                return None
            elif com != None:
                sub_register_group = readBySerial(cls, com, start, length, config, func, monitor_func)
            else:
                sub_register_group = readByTCP(self, start, length, config, func, monitor_func)
            if sub_register_group == None:
                return None
            sub = mappingReadData(sub, sub_register_group)
            groups.extend(sub)
        if not monitor_func():
            return None
        return groups
    return decorator

def writeBySerial(cls, com: 'ComData', start: int, data: List[int], 
              config: DeviceConfigFormat, func: Callable,
              monitor_func: Callable[[], bool])->bool:
    retry = 0
    write_result = False
    protocol = config.protocol_config
    max_retry = protocol['max_retry'] if 'max_retry' in protocol else 2
    with com.mutex:
        while (not write_result) and (retry < max_retry) and monitor_func():
            write_result = func(cls, start, data, config, com.port)
            retry += 1
    return write_result

def writeByTCP(self: Optional[object], start: int, data: List[int], config: DeviceConfigFormat, 
              func: Callable, monitor_func: Callable[[], bool])->bool:
    retry = 0
    write_result = False
    protocol = config.protocol_config
    max_retry = protocol['max_retry'] if 'max_retry' in protocol else 2.
    try:
        while (not write_result) and (retry < max_retry) and monitor_func():
            if self != None:
                write_result = func(self, start, data, config)
            else:
                write_result = func(start, data, config)
            retry += 1
    except Exception as e:
        logging.error(e)
    return write_result

def writeRegister(func: Callable[[int, List[int], dict, Optional['ComData']],List[int]]):
    @wraps(func)
    def decorator(*args, **kwargs)->bool:
        config: DeviceConfigFormat = kwargs.get('config')
        com: Optional['ComData'] = kwargs.get('com')
        monitor_func: Callable[[], bool] = kwargs.get('monitor_func')
        registers: List[RegisterFormat] = kwargs.get('write_data')
        if len(args) == 1:
            self = args[0]
            cls = args[0]
        else:
            self = None
            cls = None
        subgroups = createRegisterList(registers, False)
        for sub in subgroups:
            data = [register.value for register in sub]
            start = sub[0].address
            write_result = None
            if not monitor_func():
                return False
            if com != None:
                write_result = writeBySerial(cls, com, start, data, config, func, monitor_func)
            else:
                write_result = writeByTCP(self, start, data, config, func, monitor_func)
            if not write_result:
                return False
        return monitor_func()
    return decorator

from app.dependencies.com_manager import ComData
from app.dependencies.register_format import RegisterFormat