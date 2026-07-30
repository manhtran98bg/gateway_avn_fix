from app import SOFTWARE_VER, login_required, auth_header
from flask_restx import Namespace, Resource, fields
from app.internal.yaml_loader import PI_SERIAL_NUMBER
from flask import request
from app.models.databases import db, User, setupDB
from app.internal.yaml_loader import DEFAULT_USER
import subprocess, logging, os
from app.models.databases import setEnterprise
from app.dependencies.mqtt_utils import MqttTopic
from typing import Optional
from app.internal.network import getNetworkInterfaceAddrs
from app.internal.services import getMQTTConnectStatus, mqtt_internal_mutex
from app.dependencies.system_log import createLog
from app.dependencies.type_define import LogModule, WorkStatus, LogType
from app.internal.device import stopDevice

__NS_URL = 'system'
system = Namespace(__NS_URL.capitalize(), description=f'APIs for {__NS_URL}', path=f'/{__NS_URL}')
system_data = system.model('System Information', {
    'software_version': fields.String(description="return current software version of backend"),
    'enterprise': fields.String(description="return current enterprise, null if don't have any enterprise is setter"),
    'serial_number': fields.String(description="return serial number of gateway"),
})

system_update_response = system.model('System Update Response', {
    'update_password': fields.Boolean(description="True if update success"),
    'update_enterprise': fields.Boolean(description="True if update success")
})

patch_update_system = system.model('System Update Request', {
    'enterprise': fields.String(description='New enterprise'),
    'new_password': fields.String(description='New password'),
    'old_password': fields.String(description='Old password'),
})

memory = system.model('Memory', {
    'total': fields.Float(description='Total of RAM (GB)'),
    'used': fields.Float(description='Used of RAM (GB)'),
    'free': fields.Float(description='Free of RAM (GB)'),
})

cpu = system.model('CPU', {
    'cpu_load': fields.Float(description='cpu load %'),
    'number_of_core': fields.Integer(description='number of cpu')
})

system_status = system.model('System Status', {
    'ram': fields.Nested(memory),
    'disk': fields.Nested(memory),
    'cpu': fields.Nested(cpu),
    'wifi_signal': fields.Integer(description='Wifi signal strength (dBm)'),
})

def getCPU():
    num_cpu_cores = os.cpu_count()
    cpu_per_cent = None
    with open('/proc/stat') as stat_file:
        stats = stat_file.readlines()

    for line in stats:
        if line.startswith("cpu "):
            fields = line.split()
            user, nice, system, idle, iowait, irq, softirq, steal, _, _ = map(int, fields[1:])
            total = user + nice + system + idle + iowait + irq + softirq + steal
            cpu_per_cent = 100.0 - (idle * 100.0 / total)
    return {
        'cpu_load': cpu_per_cent,
        'number_of_core': num_cpu_cores
    }

def getWifiSignalStrength(interface: str = "wlan0")->Optional[int]:
    try:
        # Run the iwconfig command for the specified interface
        result = subprocess.check_output(["iwconfig", interface], universal_newlines=True)

        # Find the line that contains "Signal Level"
        signal_level_line = None
        for line in result.split('\n'):
            if "Signal level" in line:
                signal_level_line = line
                break

        if signal_level_line:
            # Extract the signal strength from the line
            signal_strength = int(signal_level_line.split("=")[2].split()[0])
            return signal_strength
        else:
            return None

    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e}")
        return None

def _getStatus()->dict:
    # Get RAM information
    ram = {}
    total_memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    # Get the used memory in bytes
    used_memory = total_memory - os.sysconf('SC_AVPHYS_PAGES') * os.sysconf('SC_PAGE_SIZE')
    # Get the free memory in bytes
    free_memory = os.sysconf('SC_AVPHYS_PAGES') * os.sysconf('SC_PAGE_SIZE')
    ram['total'] = round(total_memory / (1024 ** 3), 2)  # Convert to GB
    ram['used'] = round(used_memory / (1024 ** 3), 2)    # Convert to GB
    ram['free'] = round(free_memory / (1024 ** 3), 2)    # Convert to GB

    # Get Disk information for the root partition
    disk_stat = os.statvfs('/')

    # Calculate total, used, and free space in bytes
    total_space = disk_stat.f_frsize * disk_stat.f_blocks
    free_space = disk_stat.f_frsize * disk_stat.f_bfree
    used_space = total_space - free_space
    disk = {}
    disk['total'] = round(total_space / (1024 ** 3), 2)  # Convert to GB
    disk['used'] = round(used_space / (1024 ** 3), 2)    # Convert to GB
    disk['free'] = round(free_space / (1024 ** 3), 2)    # Convert to GB

    wifi_status = getNetworkInterfaceAddrs()
    signal = None
    for eth in wifi_status:
        if 'wl' in eth:
            wifi_stats = wifi_status[eth]
            if wifi_stats.get('enable'):
                signal = getWifiSignalStrength(eth)
                break
    return {
        'ram': ram,
        'disk': disk,
        'cpu': getCPU(),
        'wifi_signal': signal
    }

@system.route('/')
class SystemAPIs(Resource):
    method_decorators = [login_required]
    @system.expect(auth_header)
    @system.marshal_with(system_data)
    def get(self)->dict:
        _users = db.session.query(User).all()
        db.session.close()
        enterprise = _users[0].enterprise if len(_users) == 1 else None
        return {
            "software_version": SOFTWARE_VER,
            "enterprise": enterprise,
            "serial_number": PI_SERIAL_NUMBER
        }

    @system.expect(auth_header, patch_update_system,validate=True)
    @system.marshal_with(system_update_response)
    def put(self)->dict:
        body = request.get_json()
        new_password = body.get("new_password")
        old_password = body.get("old_password")
        enterprise = body.get("enterprise")
        _users = db.session.query(User).all()
        password = _users[0].password if len(_users) == 1 else None
        response = {
            'update_password': False,
            'update_enterprise': False
        }
        try:
            user = db.session.query(User).filter_by(username=DEFAULT_USER).first()
        except Exception as e:
            logging.error(e)
            return response
        if password == old_password and isinstance(new_password, str) and new_password != old_password:
            createLog(LogModule.SYSTEM, WorkStatus.SUCCESS, 
                      LogType.UPDATE, "Update New Password", False)
            response['update_password'] = True
            user.password = new_password
        if isinstance(enterprise, str) and user.enterprise != enterprise:
            createLog(LogModule.SYSTEM, WorkStatus.SUCCESS, LogType.UPDATE, 
                f"Update Enterprise from {user.enterprise} to {enterprise}", False)
            response['update_enterprise'] = True
            user.enterprise = enterprise
            setEnterprise(enterprise)
            with mqtt_internal_mutex:
                if getMQTTConnectStatus():
                    MqttTopic.reconnectMqtt()
        if response['update_enterprise'] or response['update_password']:
            db.session.commit()
        db.session.close()
        return response
    
@system.route('/status')
class SystemStatus(Resource):
    method_decorators = [login_required]
    @system.expect(auth_header)
    @system.marshal_with(system_status)
    def get(self)->dict:
        return _getStatus()
    
@system.route('/factory_reset')
class FactoryReset(Resource):
    method_decorators = [login_required]
    @system.expect(auth_header)
    def post(self):
        stopDevice()
        setupDB(True)
        createLog(LogModule.SYSTEM, WorkStatus.SUCCESS, LogType.UPDATE, 
                "Factory Reset")
        logging.info("Factory Reset Success")
        return {"message": "Factory reset successful"}