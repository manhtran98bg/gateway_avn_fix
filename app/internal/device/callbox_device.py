from ..device import MonitorDevice
from app.dependencies.type_define import DeviceTypes, ErrorCode
from typing import List, Dict, Tuple, Type
import logging, time
from app import db, redis_client, API_VERSION
from app.internal.yaml_loader import PI_SERIAL_NUMBER, LIMIT_RECORD
from app.models.databases import getEnterprise
from app.models.databases import CallBoxError
from sqlalchemy.orm.exc import NoResultFound
from app.dependencies.mqtt_utils import MqttTopic
import requests, json
from requests.auth import HTTPBasicAuth
from app.dependencies.util.time_util import get_ip
from app.dependencies.register_format import RegisterFormat

AUTO_LINE_DEVICE_ID = "device5489411b-8562-4ac2-826f-e2fccbb142b3"

@MonitorDevice.registerDevice(DeviceTypes.CALL_BOX.value, "Class for monitoring Call Box")
class CallBoxDevice(MonitorDevice):
    register_required: List[str] = ['button_{no}', 'b{no}_id', 'fb{no}']
    device_configuration: Dict[str, callable] = {
        'max_retry': lambda value: int(value) > 0,
        'enable': lambda value: isinstance(value, bool),
        'server_ip': lambda value: isinstance(value, str),
        'server_port': lambda value: isinstance(value, int) and value > 0,
        'username': lambda value: isinstance(value, str) and value != '',
        'password': lambda value: isinstance(value, str) and value != '',
        'uptime_send_time': lambda value: float(value) > 0.,
        'timeout_call_api': lambda value: float(value) > 0.,
        'timeout_when_disconnect': lambda value: float(value) > 5.,
        'number_of_button': lambda value: isinstance(value, int) and value > 0,
        'auto_feedback': lambda value: isinstance(value, bool)
    }
    def __init__(self, configure: dict, protocol: str):
        super().__init__(configure, protocol)
        self.__need_enable = True
        self.device_data = {}

        self.last_up_time = {}
        self.last_other_time = {}

        self.production_data = {}
        self.max_actual = {}
        self.led = {}
        self.number_of_button = self.device["number_of_button"]
        self.number_of_button = int(len(self.registers)/3)
        self.button_mapping = {
            f'b{i+1}_id': f'button_{i+1}'
            for i in range(self.number_of_button)
        }
        logging.error(self.button_mapping)
        for register in self.registers:
            if 'fb' in register.name:
                self.write_registers.append(register)
            self.read_registers.append(register)
        self.last_time_sync_uptime = time.time()
        self.last_time_read_success = time.time()
        self.disconnected_log = False
        self.button_information = {}
        self.uptime_data_information = {}

    @classmethod
    def updateRequired(cls: Type['CallBoxDevice'], device: Dict[str, any],
            registers: List[str])->Tuple[Dict[str, any], List[str]]:
        number_of_button = device.get('number_of_button', 1)
        extended_registers: List[str] = []
        for i in range(number_of_button):
            extended_registers.extend(
                [
                    register.replace('{no}', str(i+1))
                    for register in registers
                ]
            )
        return cls.device_configuration, extended_registers

    def getStatus(self)->dict:
        if self.button_information != {} and not self.disconnected_log:
            button_information = self.button_information
        else:
            button_information = {
                f'button_{i+1}': None
                for i in range(self.number_of_button)
            }
        leds = self.led.copy()
        led = [
            {
                "led_id": int(key[3:]),
                "action": leds[key]
            }
            for key in leds
        ]
        button = [
            {
                "button_id": int(key.split("_")[-1]),
                "action": button_information[key]
            }
            for key in button_information
        ]
        return {
            'uptime': self.uptime,
            'button': button,
            'led': led
        }

    def _readDeviceData(self)->bool:
        registers = None
        if not self.device.get('enable'):
            return True
        else:
            registers = self._readPLCRegister()
        result = False
        if registers != None:   
            self.readSuccess(registers)
            result = True
        else:
            self.readFailed()
        # if time.time() - self.last_time_sync_uptime > self.device.get('uptime_send_time'):
        #     delta_time = time.time() - self.last_time_sync_uptime
        #     self.last_time_sync_uptime = time.time()
        #     self.uptime = redis_client.hgetall(self._uptime_topic)
        #     uptime = float(self.uptime['uptime']) + delta_time
        #     redis_client.hset(self._uptime_topic, 'uptime', uptime)
        #     msg = {
        #         "gateway_id": PI_SERIAL_NUMBER,
        #         "timestamp": self.last_time_sync_uptime,
        #         "deviceId": self._id,
        #         'ip': get_ip()
        #     }
        #     led = []
        #     button = []
        #     for i in range(self.number_of_button):
        #         led.append({
        #             "led_id": i+1,
        #             "action": self.uptime_data_information.get(f'fb{i+1}')
        #         })
        #         button.append({
        #             "button_id": i+1,
        #             "action": self.uptime_data_information.get(f'button_{i+1}')
        #         })
        #     msg["led"] = led
        #     msg["button"] = button
        #     msg['plc_status'] = self.connectStatus()
        #     MqttTopic.putToQueue(f'/{API_VERSION}/{getEnterprise()}/uptime', msg)
        return result
    
    def readSuccess(self, registers: List[RegisterFormat]):
        information = {
            register.name: register.value
            for register in registers
        }
        self.uptime_data_information = information.copy()
        self.led = {}
        for i in range(self.number_of_button):
            self.led[f'led{i+1}'] = information[f'fb{i+1}']
            del information[f'fb{i+1}']
        try:
            redis_uptime = redis_client.hgetall(self._uptime_topic)
            if redis_uptime:
                self.uptime = redis_uptime
        except Exception as e:
            logging.warning(f"Redis read failed for {self._uptime_topic}. Use memory cache: {e}")
        self.disconnected_log = False
        self.last_time_read_success = time.time()
        send_to_be = {}
        save_to_redis = {}
        is_auto_line = self._id == AUTO_LINE_DEVICE_ID
        for key in self.button_mapping:
            register = self.button_mapping[key]
            if information[key] != int(self.uptime[key]):
                send_to_be[register] = information[register]
                save_to_redis[key] = information[key]
            old_action = self.button_information.get(register)
            new_action = information[register]
            if is_auto_line and old_action != new_action:
                logging.info(
                    f"Auto line PLC button state changed device_id={self._id} "
                    f"button_id={int(register.split('_')[-1])} button={register} "
                    f"old_action={old_action} new_action={new_action} "
                    f"id_register={key} old_id={self.uptime.get(key)} new_id={information[key]}"
                )
            self.button_information[register] = information[register]
        if len(send_to_be) != 0:
            self.uptime.update(save_to_redis)
            try:
                redis_client.hset(self._uptime_topic, mapping=save_to_redis)
            except Exception as e:
                logging.warning(f"Redis write failed for {self._uptime_topic}. Keep memory cache only: {e}")
            timeout_call_api = self.device.get('timeout_call_api')
            port = self.device["server_port"]
            url = f'http://{self.device["server_ip"]}:{port}/trigger'
            list_action_to_be = []
            for key in send_to_be:
                new_action = {
                    'button_id': int(key.split('_')[-1]),
                    'action': send_to_be[key]
                }
                list_action_to_be.append(new_action)
            plc_id = self._id
            send_to_be = {
                'timestamp': time.time(),
                'device_id': plc_id,
                'tasks': list_action_to_be,
                'gateway_id': PI_SERIAL_NUMBER
            }
            # TEMP: If pwm or auto line, then not send
            if plc_id == "device0fc9ab1c-61bd-495e-8a03-1025119376dd" or\
                plc_id == AUTO_LINE_DEVICE_ID:
                return
            try:
                response = requests.post(url, auth=HTTPBasicAuth(username=self.device['username'], 
                    password=self.device['password']), json=send_to_be, timeout=timeout_call_api)
                if response.status_code == 200:
                    if self.device.get('auto_feedback', False):
                        json.loads(response.text)['msg']
                        self.sendFeedbackToPLC(list_action_to_be)
                    return
            except Exception as e:
                logging.error(e)
            logging.warning(f"Device {self._id} with type {DeviceTypes.CALL_BOX.value} call server over api failed")
            self._saveErrorToDB(ErrorCode.CAN_NOT_CALL_SERVER.value, 
                f"Can not call IP to server: {self.device['server_ip']}")
            
    def sendFeedbackToPLC(self, list_fb: list):
        map_write_register = {
            register.name: register.address
            for register in self.write_registers
        }
        write_list = []
        for fb in list_fb:
            button_id = f'fb{fb["button_id"]}'
            write_list.append(RegisterFormat(
                name=button_id,
                address=map_write_register[button_id],
                value=fb['action']
            ))
        print(f"WRITE LIST {write_list}")
        self._writePLCRegister(write_list)

    def readFailed(self):
        if (time.time() - self.last_time_read_success > self.device['timeout_when_disconnect']
            and not self.disconnected_log):
            self.disconnected_log = True
            logging.warning(f"Device {self._id} with type {DeviceTypes.CALL_BOX.value} disconnect")
            self._saveErrorToDB(ErrorCode.DISCONNECTED.value, 
                f"Can not connect device {self._id} with protocol {self._protocol}")

    def _saveErrorToDB(self, code: int, desc: str):
        count_records = db.session.query(CallBoxError).filter_by().count()
        if count_records > LIMIT_RECORD:
            first_record = db.session.query(CallBoxError).first()
            db.session.query(CallBoxError).filter_by(id=first_record.id).delete()
        new_error = CallBoxError(
            device_id = self._id,
            module = DeviceTypes.CALL_BOX.value,
            code = code, 
            timestamp = time.time(),
            desc = desc
        )
        db.session.add(new_error)
        db.session.commit()
        db.session.close()

    def _getRedisData(self):
        self.number_of_button = self.device.get('number_of_button', 1)
        self._uptime_topic = f"/{DeviceTypes.CALL_BOX.value}/{API_VERSION}/{self._id}/uptime"
        self.uptime = redis_client.hgetall(self._uptime_topic)
        if not self.uptime:
            self.uptime = {
                "uptime" : 0
            }
            for i in range(self.number_of_button):
                self.uptime[f'b{i+1}_id'] = 0
        redis_client.hset(self._uptime_topic, mapping=self.uptime)
    
    def cloudSyncChangeProduct(self, payload: dict):
        logging.debug(f'Device {self._id}: {payload}')

    def cloudSyncMachine(self, payload: dict):
        error_id = payload.get('id')
        try:
            error_to_delete = CallBoxError.query.filter_by(id=error_id).one()
            db.session.delete(error_to_delete)
            logging.debug("Success: Row deleted successfully!")
        except NoResultFound:
            logging.error("Error: Row not found!")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error: {str(e)}")
        db.session.commit()
        db.session.close()

    def cloudSyncDowntime(self, payload: dict):
        logging.debug(f'Device {self._id}: {payload}')

    def cloudCmdHandle(self, payload: dict):
        logging.debug(f'Device {self._id}: {payload}')

    def cloudSettings(self, payload: dict):
        logging.debug(f'Device {self._id}: {payload}')

    def clearDataStorage(self, no_commit: bool = False):
        redis_client.delete(self._uptime_topic)
        try:
            errors_to_delete = db.session.query(CallBoxError).filter_by(device_id=self._id).all()
            for error in errors_to_delete:
                db.session.delete(error)
            if not no_commit:
                db.session.commit()
                db.session.close()
            logging.info(f"CallBoxError: Rows with device_id {self._id} deleted successfully!")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error: {str(e)}")

    def controlOverAPI(self, cmd: dict)->Tuple[bool, str]:
        write = []
        for register in self.write_registers:
            if register.name in cmd:
                write.append(RegisterFormat(
                    name=register.name,
                    address=register.address,
                    value=cmd[register.name]
                ))
        if len(write) != 0:
            if self._writePLCRegister(write):
                return True, "Write to Control box success"
            else:
                return False, "Write to Control box failed"
        return False, "Empty data to write Control box"
