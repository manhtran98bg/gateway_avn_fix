from app import login_required, auth_header
from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from app.internal.network import getNetworkInfo, updateEthernet, updateWifi, listWifiNetworks
from app.internal.yaml_loader import WIFI, ETH

__NS_URL = 'network'
network = Namespace(__NS_URL.capitalize(), description=f'APIs for {__NS_URL}', path=f'/{__NS_URL}')
network_data = network.model('Network Information', {
    'type': fields.String(description="Type of network: ethernet, wifi"),
    'mac': fields.String(description="Physical mac address"),
    'ip': fields.String(description="IP address"),
    'subnet_mask': fields.String(description="Subnet mask of gateway"),
    'dhcp': fields.Boolean(description="true if in dhcp mode"),
    'ssid': fields.String(description="ssid of wifi"),
    'signal': fields.Integer(description="signal of wifi"),
    'gateway': fields.String(description="get gateway"),
    'enable': fields.Boolean(description="Internet connection status. True if internet is available")
})
network_type_arg = reqparse.RequestParser()
network_type_arg.add_argument('network_type', required=True,choices=['eth', 'wls', None] ,help='Network type include: eth, wls')

network_setting = network.model('Network Setting Request', {
    'dhcp': fields.Boolean(description='true if when to use dhcp server'),
    'static_ip': fields.String(description='if dhcp is false, setting static ipv4 for gateway'),
    'static_subnet_mask': fields.String(description='if dhcp is false, setting static subnet mask for gateway'),
    'static_gateway': fields.String(description='if dhcp is false, setting static gateway for gateway'),
    'ssid': fields.String(description='if network_type is wifi, setting ssid of wifi'),
    'password': fields.String(description='if network_type is wifi, setting password of wifi')
})
update_status = network.model('Network Update Status', {
    'type': fields.String(description='network type'),
    'network': fields.Nested(network_setting, description="Type of network: ethernet, wifi"),
    'update': fields.Boolean(description='update status')
})
wifi_data = network.model('Wifi Details', {
    'SSID': fields.String(description='SSID of wifi'),
    'signal': fields.Integer(description='signal strength')
})

@network.route('/')
class Network(Resource):
    method_decorators = [login_required]
    @network.expect(auth_header)
    @network.marshal_with(network_data, as_list=True)
    def get(self):
        return getNetworkInfo()
    @network.expect(auth_header, network_type_arg, network_setting)
    @network.marshal_with(update_status)
    def post(self):
        network_type = request.args.get('network_type')
        body = request.json
        update = False
        if network_type == 'ethernet':
            update = updateEthernet(body)
        elif network_type == 'wifi':
            update = updateWifi(body)
        else:
            update = False
        return {
            "type": network_type,
            "network": body,
            "update": update
        }
    
@network.route('/wifi_list')
class Wifi(Resource):
    method_decorators = [login_required]
    @network.expect(auth_header)
    @network.marshal_with(wifi_data, as_list=True)
    def get(self):
        return listWifiNetworks()