from app import login_required, auth_header, db
from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.databases.gateway_db import DeviceGroup, Device
from app.dependencies.error_response import badRequestError
from app.dependencies.type_define import LogType, WorkStatus, LogModule
from app.dependencies.system_log import createLog
from app.internal.device import MonitorDevice, stopDevice
from typing import Dict
from uuid import uuid4
import logging

__NS_URL = 'device_group'
device_group_api = Namespace(__NS_URL.replace("_", " ").capitalize(), description=f'APIs for {__NS_URL.replace("_", " ")}', path=f'/{__NS_URL}')

group_name =  device_group_api.model("Group name", {
    'id': fields.String(description="ID of group"),
    'name': fields.String(description="Name of group")
})

device_details = device_group_api.model("Device details in group id", {
    'name': fields.String(description='device name'),
    'type': fields.String(description='device type'),
    'protocol': fields.String(description='protocol name'),
    'device_id': fields.String(description='device id'),
    'status': fields.String(description='device status'),
    'key': fields.Integer(description='key in fe table')
})

group_details = device_group_api.model("Group details",{
    'id': fields.String(description="ID of group"),
    'name': fields.String(description="Name of group"),
    'groups_detail': fields.List(fields.Nested(device_details), description='list device')
})

group_list = device_group_api.model("Group List",{
    'groups': fields.List(fields.Nested(group_details),description='List group'),
    'total': fields.Integer(description='Number of groups'),
})

update_group = device_group_api.model("Update Group", {
    'group_name': fields.String(description='name of group')
})

@device_group_api.route('/')
class DeviceGroupAPI(Resource):
    method_decorators = [login_required]
    @device_group_api.expect(auth_header)
    @device_group_api.marshal_with(group_list)
    def get(self):
        groups = db.session.query(DeviceGroup).all()
        list_name = []
        list_device: Dict[str, list] = {}
        for group_db in groups:
            list_name.append({
                'id': group_db.id,
                'name': group_db.name,
                'groups_detail': []
            })
            list_device[group_db.id] = []
            devices = db.session.query(Device).filter_by(
                group_id = group_db.id).all()
            i = 0
            for device in devices:
                device_id = device.id
                name = device.name
                protocol = device.protocol_type
                device_type = device.device_type
                if device_id in MonitorDevice.operator_device_list:
                    status = MonitorDevice.operator_device_list[device_id].connectStatus()
                    if status:
                        status = 'Connected'
                    else:
                        status = 'Disconnected'
                else:
                    status = "Inactivate"
                new_device = {
                    'name': name,
                    'type': device_type,
                    'protocol': protocol,
                    'device_id': device_id,
                    'status': status,
                    'key': i
                }
                i += 1
                list_name[-1]['groups_detail'].append(new_device)
        db.session.close()
        return {
            'groups': list_name,
            'total': len(list_name),
            'groups_details': list_device
        }

    @device_group_api.expect(auth_header, update_group)
    def post(self):
        """Add new group"""
        logging.error(request.get_json())
        name = request.get_json().get('group_name')
        if db.session.query(DeviceGroup).filter_by(name=name).count() == 0:
            group_id = "group" + str(uuid4())
            new_group = DeviceGroup(id = group_id,
                                    name = name)
            msg = f"Add group {name} success"
            createLog(LogModule.SYSTEM, WorkStatus.SUCCESS, LogType.UPDATE,
                msg, False)
            db.session.add(new_group)
            db.session.commit()
            db.session.close()
            logging.error(group_id)
            return {
                'message': msg,
                'id': group_id
            }
        else:
            db.session.close()
            return badRequestError(f'Group {name} is available')

@device_group_api.route('/<string:group_id>')
class UpdateGroupAPI(Resource):       
    @device_group_api.expect(auth_header)
    def delete(self, group_id: str):
        """Delete device by id"""
        delete_group = group_id
        gr = db.session.query(DeviceGroup).filter_by(id=delete_group).first()
        if gr:
            devices = db.session.query(Device).filter_by(group_id=delete_group).all()
            for device in devices:
                device_id = device.id
                if device_id in MonitorDevice.operator_device_list:
                    stopDevice(device_id, True, True)
                    db.session.query(Device).filter_by(id=device_id).delete()
            db.session.query(DeviceGroup).filter_by(id=delete_group).delete()
            msg = f"Delete group {gr.name} success"
            createLog(LogModule.SYSTEM, WorkStatus.SUCCESS, LogType.UPDATE,
                msg, False)
        else:
            msg = f"Group {delete_group} is not available"
        db.session.commit()
        db.session.close()
        return {
            'message': msg
        }
    
    @device_group_api.expect(auth_header, update_group)
    def put(self, group_id: str):
        """Change name of group"""
        put_group = group_id
        name = request.get_json().get('group_name')
        gr = db.session.query(DeviceGroup).filter_by(
            id=put_group).first()
        name_check = db.session.query(DeviceGroup).filter(
            DeviceGroup.id!=put_group,
            DeviceGroup.name==name
        ).first()
        if name_check:
            msg = f"Name {name} is duplicated"
        elif gr:
            gr.name = name
            db.session.commit()
            msg = "Update group name success"
        else:
            msg = "Can not find group id"
        return {
            'msg': msg
        }
