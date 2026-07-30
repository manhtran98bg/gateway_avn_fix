from app.internal.device import (MonitorDevice, Device, db, 
            MonitorConnection, RegisterFormat, DeviceGroup, executor)
from typing import Tuple, Optional, List, Dict
from uuid import uuid4
import logging

def postPreCheck(config: dict, name: str, group_id: str)->Tuple[bool, str]:
    device = db.session.query(Device).filter_by(name=name).first()
    default_groups = db.session.query(DeviceGroup).filter_by(id=group_id).first()
    db.session.close()
    #check required args in body
    if device != None: #check device is available, if have a device with same name return false
        return False, f'Device name: "{name}" is available'
    if default_groups == None: #check group device is available
        return False, f'Invalid Device Group: "{group_id}"'
    for arg in MonitorDevice.device_args_required: #check config provide all required config
        if arg not in config:
            return False, f'Missing Field. Create New Device need: {MonitorDevice.device_args_required}'
    registers = config.get('registers')
    device_type = config.get('type')
    protocol = config.get('protocol')
    protocol_type = config.get('protocol_type')  
    #check protocol type and device type is support          
    if (isinstance(registers, list)
            and  (device_type in MonitorDevice.device_type_list)
            and (protocol_type in MonitorConnection.protocol_list)
            and isinstance(protocol,dict)):
        return True, "Success"
    else:
        return False, "Wrong format of request body"

def postToDB(configure: dict, name: str, 
                group_id: str)->Tuple[bool, str, Optional[dict], Optional[str]]:
    return_data = {
        'type': configure.get('type'),
        'registers': [],
        'protocol': {},
        'device': {},
        'protocol_type': configure.get('protocol_type')
    }
    device_type = configure.get('type')
    registers = configure.get('registers')
    protocol_params = configure.get('protocol')
    device = configure.get('device')
    protocol = configure.get('protocol_type')
    protocol_required = MonitorConnection.createMonitorConnect(protocol).config_required
    register_required = MonitorDevice.device_type_list[device_type].register_required
    device_required, register_required = MonitorDevice.device_type_list[device_type].updateRequired(
        device, register_required)
    success, desc, return_data['registers'] = checkRegister(register_required, registers)
    #check user provide all register, that system need to monitor device
    if not success:
        return False, desc, None, None
    registers = return_data['registers']
    #check required protocol configure
    success, wrong_key, return_data['protocol'] = checkParamRequired(protocol_required, protocol_params)
    if not success:
        return False, f'Wrong/Missing param "{wrong_key}" when connect by protocol "{protocol}"', None, None
    protocol_params = return_data['protocol']
    #check configure of device
    success, wrong_key, return_data['device'] = checkParamRequired(device_required, device)
    if not success:
        return False, f'Wrong/Missing param "{wrong_key}" when setup device type: "{device_type}"', None, None
    device = return_data['device']
    #push new data to db
    new_id = "device" + uuid4().__str__()
    new_device = Device(
        id=new_id,
        name=name,
        device_type=device_type,
        group_id=group_id,
        protocol_type=protocol,
        protocol=protocol_params,
        register=registers,
        device=device
    )
    db.session.add(new_device)
    db.session.commit()
    db.session.close()
    return True, "Success", return_data, new_id

def putToDB(configure: dict, device_id: str)->Tuple[bool, Optional[str], Optional[str]]:
    device = db.session.query(Device).filter_by(id=device_id).first()
    group_id = configure.get('group_id')
    success, desc = (True, None)
    list_update = []
    if device == None:
        db.session.close()
        return False, f"Device id: {device_id} is not available", None
    if group_id != None:
        list_update.append('group')
        success, desc = updateGroupID(group_id, device)
    if not success:
        return success, desc, None
    #update protocol
    protocol_type = configure.get('protocol_type')
    protocol = configure.get('protocol')
    if isinstance(protocol, dict):
        list_update.append('protocol')
        success, desc = updateProtocol(protocol_type, protocol, device)
    if not success:
        return success, desc, None
    #update device
    device_configure = configure.get('device')
    if isinstance(device_configure, dict):
        list_update.append('device')
        success, desc = updateDeviceParam(device_configure, device)
    if not success:
        return success, desc, None
    #update register
    registers = configure.get('registers')
    if isinstance(registers, list):
        list_update.append('registers')
        success, desc = updateRegister(registers, device)
    if not success:
        return success, desc, None
    #cache database change
    group_id = device.group_id
    device_param = device.device
    device_register = device.register
    device_protocol = device.protocol
    protocol_type = device.protocol_type
    try:
        db.session.close()
    except Exception as e:
        logging.error(e)
    #update database
    device = db.session.query(Device).filter_by(id=device_id).first()
    device.device = device_param
    device.register = device_register
    device.protocol = device_protocol
    device.protocol_type = protocol_type
    device.group_id = group_id
    db.session.commit()
    db.session.close()
    return True, desc, group_id

def checkRegister(required: List[str], 
        registers: List[dict])->Tuple[bool, Optional[str], Optional[List[dict]]]:
    total_required = len(required)
    list_register = []
    name_register = []
    return_data = []
    for register in registers:
        name = register['name']
        addr = register['addr']
        right_type = isinstance(name, str) and isinstance(addr, int)
        # checking missing required register
        if (name in required and addr not in list_register 
            and right_type and name not in name_register):
            total_required += -1
            list_register.append(addr)
            name_register.append(name)
            return_data.append({
                'name': name,
                'addr': addr
            })

    if total_required != 0:
        return False, f'Device need register: {required} with different register address', None
    else:
        return True, None, return_data
    

def checkParamRequired(required: Dict[str, callable],
        input: dict)->Tuple[bool, Optional[str], Optional[dict]]:
    try:
        output = {}
        for key in required:
            param = input.get(key)
            if not required[key](param):
                return False, key, None
            output[key] = param
        return True, None, output
    except Exception as e:
        logging.error(e)
        return False, key, None
    
def updateGroupID(group_id: str, device: Device)->Tuple[bool, Optional[str]]:
    device_group = db.session.query(DeviceGroup).filter_by(id=group_id).first()
    if device_group == None:
        db.session.close()
        return False, f"Group id: {group_id} is not available"
    device.group_id = group_id
    return True, None

def updateProtocol(protocol_type: str, protocol: dict, device: Device)->Tuple[bool, Optional[str]]:
    if protocol_type == None or protocol_type == device.protocol_type:
        old_protocol = device.protocol
        old_protocol.update(protocol)
        protocol_required = MonitorConnection.createMonitorConnect(device.protocol_type).config_required
        success, wrong_key, new_protocol = checkParamRequired(protocol_required, old_protocol)
        if not success:
            db.session.close()
            return False, f'Wrong/Missing param "{wrong_key}" when connect by protocol "{protocol}"'
        else:
            device.protocol = new_protocol
            return True, None
    elif protocol_type not in MonitorConnection.protocol_list:
        db.session.close()
        return False, f"Protocol: {protocol_type} is not supported"
    else:
        protocol_required = MonitorConnection.createMonitorConnect(protocol_type).config_required
        success, wrong_key, new_protocol = checkParamRequired(protocol_required, protocol)
        if not success:
            db.session.close()
            return False, f'Wrong/Missing param "{wrong_key}" when connect by protocol "{protocol}"'
        else:
            device.protocol = new_protocol
            device.protocol_type = protocol_type
            return True, None
        

def updateRegister(registers:list, device: Device)->Tuple[bool, Optional[str]]:
    old_register = {
        register['name']: register['addr'] for register in device.register
    }
    new_register = {
        register['name']: register['addr'] for register in registers
    }
    old_register.update(new_register)
    new_register = [
        {
            'name': key,
            'addr': old_register[key]
        } for key in old_register
    ]
    device_object = MonitorDevice.device_type_list[device.device_type]
    register_required = device_object.register_required
    _, register_required = device_object.updateRequired(device.device, register_required)
    success, desc, new_register = checkRegister(register_required, new_register)
    if not success:
        db.session.close()
        return False, desc
    device.register = new_register
    return True, None

def updateDeviceParam(device_configure: dict, device: Device):
    old_param = device.device
    old_param.update(device_configure)
    device_required = MonitorDevice.device_type_list[device.device_type].device_configuration
    logging.error(old_param)
    success, wrong_key, new_param = checkParamRequired(device_required, old_param)
    if not success:
        db.session.close()
        msg = f'Wrong/Missing param "{wrong_key}" when setup device type: "{device.device_type}"'
        return False, msg
    device.device = new_param
    return True, None

def createDeviceByID(device_id: str)->MonitorDevice:
    device = db.session.query(Device).filter(Device.id == device_id)
    db.session.close()
    if device != None:
        device = device[0]
        protocol_type = device.protocol_type
        device_type = device.device_type
        configure = {
            'device_id': device_id,
            'device': device.device,
            'protocol': device.protocol,
            'register': device.register,
            'protocol_type': device.protocol_type
        }
        return MonitorDevice.device_type_list[device_type](configure, protocol_type)
    
def startMonitor(device_id: str, device: MonitorDevice):
    if device_id not in MonitorDevice.operator_device_list:
        MonitorDevice.operator_device_list[device_id] = device
        executor.submit(device.start)

def stopMonitor(device_id: str):
    if device_id in MonitorDevice.operator_device_list:
        device = MonitorDevice.operator_device_list[device_id]
        device.stop()
        try:
            device.__del__()
        except Exception as e:
            logging.error(e)
        del MonitorDevice.operator_device_list[device_id]

def startDevice(devices: Optional[str] = None, get_type:bool = False)->Optional[str]:
    if devices == None:
        devices = db.session.query(Device).all()
    else:
        devices = db.session.query(Device).filter_by(id = devices)
    db.session.close()
    device_type = None
    if devices != None:
        for device in devices:
            monitor = createDeviceByID(device.id)
            startMonitor(device.id, monitor)
            if get_type:
                device_type = device.device_type
    return device_type

def stopDevice(device: Optional[str] = None, clear_data: bool = False, no_commit:bool = False):
    if device == None:
        for device_name in MonitorDevice.operator_device_list:
            MonitorDevice.operator_device_list[device_name].stop()
        MonitorDevice.operator_device_list.clear()
    elif device in MonitorDevice.operator_device_list:
        MonitorDevice.operator_device_list[device].stop()
        if clear_data:
            MonitorDevice.operator_device_list[device].clearDataStorage(no_commit)
        del MonitorDevice.operator_device_list[device]