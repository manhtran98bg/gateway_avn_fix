from app import login_required, auth_header, db, logging
from flask_restx import Namespace, Resource, fields, reqparse
from flask import request, abort
from app.models.databases.gateway_db import Device
from app.dependencies.type_define import DeviceTypes
from app.internal.device import (MonitorDevice, startMonitor, stopDevice, startDevice,
                                postToDB, postPreCheck, putToDB, createDeviceByID)
from app.dependencies.error_response import badRequestError, requiredBody
from app.dependencies.type_define import LogType, WorkStatus
from app.dependencies.system_log import createLog

__NS_URL = 'device'
device = Namespace(__NS_URL.capitalize(), description=f'APIs for {__NS_URL}', path=f'/{__NS_URL}')
device_type_values = [member.value for member in DeviceTypes]
device_register = device.model('Register', {
    'name': fields.String(description='Name of register'),
    'addr': fields.Integer(description='Address of register')
})

device_protocol = device.model('Protocol',{
    'name': fields.String(description='Name of param'),
    'value': fields.Raw(description='Value of it')
})

device_detail = device.model('Device Details',{
    'type': fields.String(description='Type of device'),
    'registers': fields.List(fields.Nested(device_register), description='Register for monitoring'),
    'protocol': fields.Raw(description='Protocol for monitoring'),
    'device': fields.Raw(description='Configuration for device'),
    'protocol_type': fields.String(description='Type of protocol'),
    'name': fields.String(description='Name of device')
})

update_detail = device.model('Device Update',{
    'group_id': fields.String(description='Group of device'),
    'registers': fields.List(fields.Nested(device_register), description='Register for monitoring'),
    'protocol': fields.Raw(description='Protocol for monitoring'),
    'device': fields.Raw(description='Configuration for device'),
    'protocol_type': fields.String(description='Type of protocol')
})

devices_data = device.model('Device Information', {
    'device_group': fields.String(description="Group of device"),
    'id': fields.String(description="ID of device"),
    'connect_status': fields.Boolean(description='Device connection status'),
    'detail': fields.Nested(device_detail, description='Details information of device')
})

update_device = device.model("Change Device Success",{
    'desc': fields.String(description='Notification when success.'),
    'device_id': fields.String(description='ID of device. that is created/updated.'),
    'group_id': fields.String(description='Group contain deice')
})

control_model = device.model('Control device', {
    # 'data': fields.Raw(required=True, description='A dictionary with any format')
})

types = reqparse.RequestParser()
types.add_argument('type', choices=device_type_values, help="Filter by type. Device's type include: oee, env, electric")

groups = reqparse.RequestParser()
groups.add_argument('group_id', help="Filter by group devices")

device_id = reqparse.RequestParser()
device_id.add_argument('device_id', help="device id for access data")

device_id_required = reqparse.RequestParser()
device_id_required.add_argument('device_id', help="device id for access data", required=True)

group_id_required = reqparse.RequestParser()
group_id_required.add_argument('group_id', help="Group id of device", required=True)

@device.route('/')
class DeviceManagerAPI(Resource):
    method_decorators = [login_required]
    @device.expect(auth_header, types, groups, device_id)
    @device.marshal_with(devices_data, as_list=True)
    def get(self):
        id_device = request.args.get('device_id')
        device_type = request.args.get('type')
        device_group = request.args.get('group_id')
        filtered_devices = []
        logging.error(request.args)
        # Query the devices from the database and filter based on query parameters
        query = db.session.query(Device)
        if id_device != None:
            query = query.filter(Device.id == id_device)
        if device_type != None:
            query = query.filter(Device.device_type == device_type)
        if device_group != None:
            query = query.filter(Device.group_id == device_group)
        filtered_devices = query.all()
        db.session.close()
        return_data = []
        logging.error(MonitorDevice.operator_device_list)
        for device in filtered_devices:
            if device.id in MonitorDevice.operator_device_list:
                connect_status = MonitorDevice.operator_device_list[device.id].connectStatus()
            return_data.append({
                'device_group': device.group_id,
                'id': device.id,
                'connect_status': connect_status,
                'detail': {
                    'type': device.device_type,
                    'registers':device.register,
                    'protocol':device.protocol,
                    'device':device.device,
                    'protocol_type':device.protocol_type,
                    'name': device.name
                }
            })
        return return_data

    @device.expect(auth_header, device_id_required, update_detail)
    @device.marshal_with(update_device)
    def put(self):
        device_id = request.args.get('device_id')
        data = request.get_json()
        success, desc, group_id = putToDB(data, device_id)
        if not success:
            badRequestError(desc)
        else:
            stopDevice(device_id)
            device_type = startDevice(device_id, True)
            createLog(device_type, WorkStatus.SUCCESS, LogType.UPDATE,
                f"Update {device_type} with ID {device_id} in group {group_id}")
            return {
                'desc': f'Success When create monitoring "{device_id}" in group "{group_id}"',
                'device_id': device_id,
                'group_id': group_id
            }
    
    @device.expect(auth_header, group_id_required, device_detail)
    @device.marshal_with(update_device)
    @requiredBody
    def post(self):
        group_id = request.args.get('group_id')
        data = request.get_json()
        device_name = data.get('name')
        logging.info(data)
        check_field, desc = postPreCheck(data, device_name, group_id)
        if not check_field:
            return badRequestError(desc)
        add_to_db, desc, data, device_id = postToDB(data, device_name, group_id)
        if not add_to_db:
            logging.error(desc)
            return badRequestError(desc)
        new_device = createDeviceByID(device_id)
        if new_device == None:
            return badRequestError("Failed when create device.")
        else:
            startMonitor(device_id, new_device)
            device_type = data.get('type')
            createLog(device_type, WorkStatus.SUCCESS, LogType.ADD_DEVICE,
                f"Create {device_type} with name {device_name}")
            return {
                'desc': f'Success When create monitoring for {device_name}',
                'device_id': device_id,
                'group_id': group_id
            }

    @device.expect(auth_header, device_id_required)
    @device.marshal_with(update_device)
    def delete(self):
        device_id = request.args.get('device_id')
        device = Device.query.filter_by(id=device_id).first()
        if device != None:
            group_id = device.group_id
            createLog(device.device_type, WorkStatus.SUCCESS, LogType.DELETE,
                f"Delete {device.device_type} with ID {device_id} in group {group_id}", False)
            stopDevice(device_id, True)
            db.session.delete(device)
            db.session.commit()
            db.session.close()
            return {
                'desc': f'Delete device "{device_id}" in group "{group_id}"',
                'device_id': device_id,
                'group_id': group_id,
            }
        else:
            return badRequestError(f'Device with id: {device_id} is not available')

global abcdef_nghia
abcdef_nghia = 0
@device.route('/<string:device_id>/')
class DeviceStatus(Resource):
    method_decorators = [login_required]
    @device.expect(auth_header)
    def get(self, device_id: str):
        if device_id not in MonitorDevice.operator_device_list:
            logging.warning(f"NGHIA LOG: SOMEHOW DEVICE REMOVED {device_id}\n{MonitorDevice.operator_device_list}")
            return {'message': 'Device ID is not available'}
        else:
            data = MonitorDevice.operator_device_list[device_id].getStatus()

            # global abcdef_nghia
            # abcdef_nghia += 1
            # if abcdef_nghia >= 20:
            #     abcdef_nghia = 0
            #     logging.warning(f"458lkje == {data} ==")
            return data
        
@device.route('/control/<string:device_id>/')
class DeviceStatus(Resource):
    method_decorators = [login_required]
    @device.expect(auth_header, control_model)
    def post(self, device_id: str):
        cmd = request.get_json()
        if device_id not in MonitorDevice.operator_device_list:
            return {'message': 'Device ID is not available'}
        result, desc = MonitorDevice.operator_device_list[device_id].controlOverAPI(cmd)
        if result:
            return {
                'msg': desc
            }
        else:
            abort(400, desc)