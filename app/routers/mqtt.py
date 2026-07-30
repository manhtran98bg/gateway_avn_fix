from app import login_required, auth_header
from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from app.models.databases import db, User
from app.dependencies.mqtt_utils import MqttTopic
from app.internal.services import getMQTTConnectStatus, mqtt_internal_mutex
from app.dependencies.type_define import LogType, WorkStatus, LogModule
from app.dependencies.system_log import createLog

__NS_URL = 'mqtt'
mqtt = Namespace(__NS_URL.upper(), description=f'APIs for {__NS_URL.upper()}', path=f'/{__NS_URL}')
mqtt_data = mqtt.model('MQTT Information', {
    'username': fields.String(description="Provide MQTT username if it is required"),
    'password': fields.String(description="Length of current password"),
    'host': fields.String(description="MQTT broker IP"),
    'port': fields.Integer(description="MQTT broker port"),
    'connect_status': fields.Boolean(description="Connect status")
})

mqtt_put = mqtt.model('MQTT Change Data', {
    'username': fields.String(description="Provide MQTT username if it is required"),
    'password': fields.String(description="Provide MQTT password if it is required"),
    'host': fields.String(description="MQTT broker IP"),
    'port': fields.Integer(description="MQTT broker port"),
})

mqtt_sending = reqparse.RequestParser()
mqtt_sending.add_argument('topic', help="Topic to publish to broker", required=True)
mqtt_sending.add_argument('payload', help="Topic to publish to broker", required=True)

def getMQTTInfo(status: bool)->dict:
    user = db.session.query(User).all()[0]
    output = {
        'username': user.mqtt_username,
        'password': user.mqtt_password,
        'host': user.mqtt_host,
        'port': user.mqtt_port,
        'connect_status': status
    }
    db.session.close()
    return output

@mqtt.route('/')
class MqttAPIs(Resource):
    method_decorators = [login_required]
    @mqtt.expect(auth_header)
    @mqtt.marshal_with(mqtt_data)
    def get(self)->dict:
        return getMQTTInfo(getMQTTConnectStatus())
    
    @mqtt.expect(auth_header, mqtt_put, validate=True)
    @mqtt.marshal_with(mqtt_data)
    def put(self):
        body = request.get_json()
        username = body.get("username")
        password = body.get("password")
        host = body.get("host")
        port = body.get("port")
        user = db.session.query(User).all()[0]
        update = []
        if isinstance(host, str) and user.mqtt_host != host:
            user.mqtt_host = host
            update.append('host')
        if isinstance(port, int) and user.mqtt_port != port:
            user.mqtt_port = port
            update.append('port')
        if isinstance(username, str) and user.mqtt_username != username:
            user.mqtt_username = username
            update.append('username')
        if isinstance(password, str) and user.mqtt_password != password:
            user.mqtt_password = password
            update.append('password')
        if len(update) != 0:
            createLog(LogModule.MQTT, WorkStatus.SUCCESS, LogType.UPDATE,
                f'Update mqtt broker information {update}', False)
            db.session.commit()
        with mqtt_internal_mutex:
            if getMQTTConnectStatus():
                MqttTopic.reconnectMqtt()
        return getMQTTInfo(False)
    
@mqtt.route('/send_message')
class MqttTestSendMsgs(Resource):
    method_decorators = [login_required]
    @mqtt.expect(auth_header, mqtt_sending)
    @mqtt.marshal_with(mqtt_data)
    def post(self):
        global MQTT_CONNECTED_STATUS
        topic = request.args.get('topic')
        payload = request.args.get('payload')
        if isinstance(topic, str) and isinstance(payload, str):
            MqttTopic.putToQueue(topic, payload)
        return getMQTTInfo(getMQTTConnectStatus())