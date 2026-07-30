from app import app, SOFTWARE_VER, PREFIX
from flask_restx import Api

api = Api(app, version=f'{SOFTWARE_VER}', title='Rostek Gateway API Doc', description='Gateway API documents', prefix=f'/{PREFIX}')

from .system import system
from .mqtt import mqtt
from .network import network
from .log import log
from .device import device
from .device_group import device_group_api
from .authn import authn

api.add_namespace(system)
api.add_namespace(mqtt)
api.add_namespace(network)
api.add_namespace(log)
api.add_namespace(device_group_api)
api.add_namespace(device)
api.add_namespace(authn)