import logging, json, threading
from app.internal.services import assignTask, BaseService
from app.models.databases.gateway_db import User
from app import app
from flask_mqtt import Mqtt, MQTT_ERR_SUCCESS
from typing import Tuple, Dict, Any
from app.internal.yaml_loader import API_VERSION, MAXIMUM_SEND_FAILED, DEFAULT_PORT
from paho.mqtt.client import Client, MQTTMessage
from app.models.databases import getEnterprise
from app.dependencies.mqtt_utils import MqttTopic
from app import db
from app.dependencies.type_define import DeviceTypes, MqttInternalTopic
from app.models.databases import Device

app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['MQTT_KEEPALIVE'] = 60 # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['MQTT_CLEAN_SESSION'] = True
MQTT_CONNECTED_STATUS:bool = False
mqtt_internal_mutex = threading.Lock()
def setMQTTConnectStatus(status: bool):
    global MQTT_CONNECTED_STATUS
    if isinstance(status, bool):
        MQTT_CONNECTED_STATUS = status
    else:
        raise ValueError('MQTT status must is boolean')
def getMQTTConnectStatus()->bool:
    global MQTT_CONNECTED_STATUS
    return MQTT_CONNECTED_STATUS
# @assignTask('mqtt loop', 'mqtt loop process')
class MqttProcess(BaseService):

    def stop(self):
        MqttTopic.reconnectMqtt()
        return super().stop()

    def _loop(self):
        logging.info("Start MQTT Loop")
        while self.keep_run:
            _user = db.session.query(User).all()[0]
            logging.debug(f"MQTT {_user.mqtt_host} {_user.mqtt_port}")
            db.session.close()
            setMQTTConnectStatus(False)
            MqttTopic.send_queue.block()
            mqtt = self.mqttConnect()
            if mqtt == None:
                continue
            self.mqtt_setup(mqtt)
            MqttTopic.send_queue.unblock()
            self.mqtt_publisher(mqtt)

    def mqttConnect(self)->Mqtt:
        mqtt = None
        global mqtt_internal_mutex
        first_loop = True
        while (mqtt == None and self.keep_run) or first_loop:
            first_loop = False
            if not MqttTopic.send_queue.empty():
                MqttTopic.send_queue.get(False)
            _user = db.session.query(User).all()[0]
            broker = _user.mqtt_host
            port = _user.mqtt_port
            port = port if (port != None) else DEFAULT_PORT
            username = _user.mqtt_username
            password = _user.mqtt_password
            db.session.close()
            if broker == None:
                logging.warn("Broker is null. Please enter broker address")
                MqttTopic.send_queue.sleep(2.)
            else:
                app.config['MQTT_BROKER_URL'] = broker
                app.config['MQTT_BROKER_PORT'] = int(port)
                app.config['MQTT_USERNAME'] = username
                app.config['MQTT_PASSWORD'] = password
                try:
                    with mqtt_internal_mutex:
                        logging.info("-- Try connect to mqtt --")
                        mqtt = Mqtt(app)
                        setMQTTConnectStatus(True)
                except Exception as e:
                    logging.error(str(e))
                    MqttTopic.send_queue.sleep(2.)
        logging.info(f'Connect With MQTT Broker Success: {broker}:{int(port)}')
        return mqtt
    
    def mqtt_setup(self, mqtt: Mqtt):
        mqtt.subscribe(f'/{API_VERSION}/{getEnterprise()}/sync')
        mqtt.subscribe(f'/{API_VERSION}/{getEnterprise()}/cmd')
        devices = db.session.query(Device).filter_by(device_type=DeviceTypes.OEE)
        db.session.close()
        for device in devices:
            topic = f"/{device.id}/setting"
            mqtt.subscribe(topic)
        @mqtt.on_connect()
        def handle_connect(client: Client, user_data: Any, flags: Dict[str, Any], rc: int):
            logging.info("ON CONNECT")
            
        @mqtt.on_message()
        def handle_mqtt_message(client: Client, user_data: Any, message: MQTTMessage):
            topic=message.topic
            payload=message.payload.decode()
            logging.debug(f"{topic} -- {payload}")
            type_msgs = topic.split('/')[-1]
            if type_msgs == "sync":
                synProcess(payload)
            elif type_msgs == "cmd":
                try:
                    cmdHandler(payload)
                    payload
                except Exception as e:
                    logging.error(str(e))
            elif type_msgs == 'setting':
                settingProcess(payload, topic)

    def mqtt_publisher(self, mqtt:Mqtt):
        error_cnt = 0
        while error_cnt < MAXIMUM_SEND_FAILED and self.keep_run:
            data = MqttTopic.send_queue.get()
            qos = data.qos
            topic = data.topic
            payload = data.data
            if not data.internal and isinstance(payload, str) or isinstance(payload, dict):
                payload = payload if isinstance(payload, str) else json.dumps(payload)
                pubData(topic, payload, qos, error_cnt, mqtt)
            elif data.internal and topic == MqttInternalTopic.UPDATE:
                mqtt.unsubscribe_all()
                mqtt = None
                return
            elif data.internal and topic == MqttInternalTopic.SUB:
                subNew(payload, mqtt)
            elif data.internal and topic == MqttInternalTopic.UNSUB:
                unsubDevice(payload, mqtt)

from app.internal.device import MonitorDevice
no_device_available = 'No device id available'
def synProcess(payload: str):
    try:
        data = json.loads(payload)
        device_id = data.get('deviceId')
        if device_id not in MonitorDevice.operator_device_list:
            logging.debug(no_device_available)
        elif data["type"] == "sync_production":
            MonitorDevice.operator_device_list[device_id].cloudSyncChangeProduct(data)
        elif data["type"] == "sync_machine":
            MonitorDevice.operator_device_list[device_id].cloudSyncMachine(data)
        elif data["type"] == "sync_downtime":
            MonitorDevice.operator_device_list[device_id].cloudSyncDowntime(data)
        logging.debug(f"delete ->> {payload}")
    except Exception as e:
        logging.error(str(e))

def settingProcess(payload: str, topic: str):
    try:
        data = json.loads(payload)
        device_id = topic.split('/')[1]
        if device_id not in MonitorDevice.operator_device_list:
            logging.warn(no_device_available)
        else:
            MonitorDevice.operator_device_list[device_id].cloudSettings(data)
    except Exception as e:
        logging.error(e)

def cmdHandler(payload: str):
    try:
        data = json.loads(payload)
        device_id = data.get('deviceId')
        if device_id not in MonitorDevice.operator_device_list:
            logging.warn(no_device_available)
        else:
            MonitorDevice.operator_device_list[device_id].cloudCmdHandle(data)
    except Exception as e:
        logging.error(e)

def subNew(id: str, mqtt: Mqtt):
    try:
        topic = f"/{id}/setting"
        mqtt.subscribe(topic)
    except Exception as e:
        logging.error(e)

def unsubDevice(id: str, mqtt: Mqtt):
    try:
        topic = f"/{id}/setting"
        mqtt.unsubscribe(topic)
    except Exception as e:
        logging.error(e)

def pubData(topic: str, payload: str, qos: int, error_cnt: int, mqtt: Mqtt)->int:
    try:
        payload = json.dumps(payload) if isinstance(payload, dict) else payload
        result = mqtt.publish(topic, payload.encode(), qos=qos)
        if result[0] != MQTT_ERR_SUCCESS:
            error_cnt += 1
    except Exception as e:
        logging.error(e)
        error_cnt += 1
    return error_cnt