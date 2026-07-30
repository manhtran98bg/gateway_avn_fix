from . import MonitorDevice
from app.dependencies.type_define import DeviceTypes
from app.models.databases.oee import (OEE, OEEProduction,
                                      OEEDowntime, OEESyncData)
from app.models.databases import  Device
from typing import List, Optional, Dict, Tuple, Type
from time import time
from app import redis_client, db
from app.dependencies.type_define import STATUS
import logging
from app.internal.yaml_loader import LIMIT_RECORD, API_VERSION
from app.models.databases import getEnterprise
from app.dependencies.mqtt_utils import MqttTopic
import json
from app.dependencies.util.time_util import get_ip, get_uptime
from app.dependencies.type_define import DeviceTypes
from app.dependencies.register_format import RegisterFormat

@MonitorDevice.registerDevice(DeviceTypes.OEE.value, "Class for monitoring OEE")
class OEEDevice(MonitorDevice):
    register_required: List[str] = ['status', 'actual', 'change_product', 'error']
    device_configuration: Dict[str, callable] = {
        'max_retry': lambda value: isinstance(value, int) and value > 0,
        'uptime_interval': lambda value: float(value) > 0,
        'scan_interval': lambda value: float(value) > 0
    }
    def __init__(self, configure: dict, protocol: str):
        super().__init__(configure, protocol)
        self.read_registers.extend(self.registers)

    @classmethod
    def updateRequired(cls: Type['OEEDevice'], device: Dict[str, any],
            registers: List[str])->Tuple[Dict[str, any], List[str]]:
        return cls.device_configuration, registers

    def _getRedisData(self):
        self._production_topic = f"/{DeviceTypes.OEE.value}/{API_VERSION}/{self._id}/production"
        self._raw_topic = f"/{DeviceTypes.OEE.value}/{API_VERSION}/{self._id}/raw"
        self.production_data = redis_client.hgetall(self._production_topic)
        if not self.production_data:
            self.production_data = {
                "runningNumber" : 0,
                "start_time" : time(),               # => start testing mode
                "start_production_time" : time(),    # start manufacturing
                "end_time" : 0,                  # end manufacturing
                "actual": 0                     # number of product in a period         
            }
            self._saveRawDataToRedis(self._production_topic, self.production_data)
        for key in self.production_data:
            self.production_data[key] = round(float(self.production_data[key]))
        
        self.device_data = redis_client.hgetall(self._raw_topic)
        self.device_data["timestamp"] = time()

        if "maxActual" not in self.device_data:
            self.device_data["runningNumber"] = 0
            self.device_data["status"] = STATUS.DISCONNECT.value
            self.device_data["actual"] = 0
            self.device_data["ng"] = 0
            self.device_data["changeProduct"] = 0
            self.device_data["lastChangeStatus"] = int(time())
            self.device_data["lastOtherTime"] = int(time())
            self.device_data["lastUptime"] = int(time())
            self.device_data["maxActual"] = 0
        else:
            for key in self.device_data:
                if key != "Device_id":
                    self.device_data[key] = int(float(self.device_data[key]))

    def getStatus(self)->dict:
        return {
            'production': self.production_data,
            'device_data': self.device_data,
        }
    
    def _getStatus(self, error: int, status: int)->int:
        if error != 0:
            status = STATUS.ERROR.value
        elif status == 0:
            status = STATUS.IDLE.value
        else:
            status = STATUS.RUN.value
        return status

    def _readRegisterSuccess(self, registers: List[RegisterFormat]):
        output = {}
        for register in registers:
            output[register.name] = register.value
        time_now = round(time())
        status = output['status']
        error = output['error']
        status = self._getStatus(error, status)
        actual = output['actual']
        changeover = output['change_product']
        prev_change = self.device_data['changeProduct']
        logging.debug(f"read from {self._id}: {status} - {actual} - {changeover}")
        self.device_data["maxActual"] = max(self.device_data["maxActual"] , actual)

        production_change = self.productionChangeCheck(prev_change, changeover, time_now)

        if  production_change:
            logging.debug('production change')
            self._saveProductionToRedis()
        last_status = self.device_data["status"]
        status_change = last_status != status
        running_number = int(self.production_data["runningNumber"])
        if status_change and  (changeover != 2):
            logging.info(f"Device {self._id} : change status")
            last_change_status = self.device_data["lastChangeStatus"]
            if status == 1: # -> Other state to 1
                duration = time_now - max(last_change_status, self.production_data["start_time"])
                if duration >= 15 :
                    logging.info("this is downtime")
                    new_downtime = OEEDowntime(
                        device_id = self._id,
                        machine_status = last_status,
                        timestamp = last_change_status,
                        duration = duration,
                        end_time = time_now,
                        running_number = running_number
                    )
                    db.session.add(new_downtime)
                    db.session.commit()
                    db.session.close()
            self.device_data["lastChangeStatus"] = time_now
        actual_change = (self.device_data['actual'] != actual)
        product_change = self.device_data['changeProduct'] != changeover
        up_time = round(time_now - int(self.production_data["start_production_time"]))

        self.device_data["timestamp"] = time_now

        if (time_now - self.device_data["lastUptime"] >= self.device['uptime_interval']) and  (changeover != 2):
            logging.debug(f"Uptime >> {self._id} RunningNumber = {running_number}, Status = {status}, changeover = {changeover}, actual = {actual}")
            send_data = {
                "deviceId" : self._id,
                "upTime" : up_time,
                "runningNumber" : running_number,
                "changeover" : changeover,
                "actual" : actual,
                "status" : status
            }
            MqttTopic.putToQueue(f"/{API_VERSION}/{getEnterprise()}/uptime", send_data, 1)
            self.device_data["lastUptime"] = time_now

        change_type = 0
        if status_change:
            change_type = 1
        if actual_change:
            change_type += 10
        if product_change:
            change_type += 100
        self._saveSyncMachineData( status, actual, time_now, 
                                  running_number, changeover, up_time, change_type)
        
        self.device_data["status"] = status
        self.device_data["actual"] = actual
        self.device_data["changeProduct"] = changeover

    def productionChangeCheck(self, prev_change: int, cur_change: int, time_now: int)->bool:
        production_change = True
        if (prev_change == 2 ) and (cur_change == 0):
            logging.info("Dung -> THU:")
            #Start new production period
            self.production_data["runningNumber"] += 1 # increase running number for new period
            self.production_data["actual"] = 0
            self.production_data["start_production_time"] = time_now
            self.production_data["end_time"] = 0
            self.production_data["start_time"] = time_now # start
            self.device_data["maxActual"] = 0
            logging.debug(self.production_data)
        elif (prev_change == 0 ) and (cur_change == 1):
            logging.info("Thu -> SX")
            self.production_data["start_production_time"] = time_now
            self.device_data["maxActual"] = 0
            logging.debug(self.production_data)
        elif (prev_change == 1 ) and (cur_change == 0):
            logging.info("SX -> THU:")
            self.production_data["end_time"] = time_now
            self.production_data["actual"] = self.device_data["maxActual"]
            # save data
            self._saveProductionData(self.production_data)
            # start new period
            self.production_data["runningNumber"] += 1 # increase running number for new period
            self.production_data["start_time"] = time_now
            self.production_data["start_production_time"] = self.production_data["start_time"]
            self.production_data["actual"] = 0
            self.production_data["end_time"] = 0
            self.device_data["maxActual"] = 0
            logging.debug(self.production_data)

        elif (prev_change == 0 ) and (cur_change == 2):
            logging.info(f"Thu -> Dung: {self.production_data}")
            self.production_data["end_time"] = time_now
            self.production_data["start_production_time"] = self.production_data["end_time"]
            self.production_data["actual"] = self.device_data["maxActual"]
            
        ##-- add
        elif (prev_change == 1 ) and (cur_change == 2):
            logging.info(f"SX -> DUNG: {self.production_data}")
            self.production_data["end_time"] = time_now
            self.production_data["actual"] = self.device_data["maxActual"]
            self._saveProductionData(self.production_data)
            self.device_data["maxActual"] = 0

        elif (prev_change == 2 ) and (cur_change == 1):
            # start new period
            logging.info(f"Dung -> SX: {self.production_data}")
            self.device_data["maxActual"] = 0
            self.production_data["runningNumber"] += 1 # increase running number for new period
            self.production_data["start_time"] = time_now
            self.production_data["start_production_time"] = self.production_data["start_time"]
            self.production_data["actual"] = 0
            self.production_data["end_time"] = 0
        else:
            production_change = False

        return production_change
    
    def _readRegisterFailed(self):
        self.device_data["status"] = STATUS.DISCONNECT.value

    def _readDeviceData(self)->bool:
        registers = self._readPLCRegister()
        return_value = False
        try:
            if registers != None:
                self._readRegisterSuccess(registers)
                return_value = True
            else:
                self._readRegisterFailed()
                return_value = False
            self._saveRawDataToRedis(self._raw_topic, self.device_data)
        except Exception as e:
            logging.error(e)
        return return_value

    def _saveRawDataToRedis(self, topic: str, data: Optional[dict]):
        if isinstance(data, dict):
            for key in data.keys():
                redis_client.hset(topic, key, data[key])

    def _saveProductionToRedis(self):
        self._saveRawDataToRedis(self._production_topic, self.production_data)

    def _saveProductionData(self, data: dict):
        count_records = db.session.query(OEEProduction).count()
        if count_records > 1000:
            first_record = db.session.query(OEEProduction).first()
            db.session.query(OEEProduction).filter_by(id=first_record.id).delete()
        insert_data = OEEProduction(
            device_id = self._id, 
            start_time = data['start_time'],
            start_production_time = data['start_production_time'],
            end_time = data['end_time'],
            actual = data['actual'],
            running_number = data["runningNumber"]
        )
        db.session.add(insert_data)
        db.session.commit()
        db.session.close() 
        logging.debug(f"Saving production Data: {data}")

    def _saveSyncMachineData(self, status: int, actual: int, time_now: int, 
                               running_number: int, changeover: int, up_time: int, change_type: int):
        if change_type == 0:
            return
        count_records = db.session.query(OEE).count()
        if count_records > LIMIT_RECORD:
            first_record = db.session.query(OEE).first()
            db.session.query(OEE).filter_by(id=first_record.id).delete()
            count_records_sync = db.session.query(OEESyncData).count()
            if count_records_sync > LIMIT_RECORD:
                first_record_sync = db.session.query(OEESyncData).first()
                db.session.query(OEESyncData).filter_by(id=first_record_sync.id).delete()
        insert_data = OEE(
            device_id = self._id, 
            machine_status = status,
            actual = actual,
            timestamp = time_now,
            running_number = running_number,
            changeover = changeover,
            up_time = up_time,
            change_type = change_type
        )

        insert_un_synced_data = OEESyncData(
            device_id = self._id, 
            machine_status = status,
            actual = actual,
            timestamp = time_now,
            running_number = running_number,
            changeover = changeover,
            up_time = up_time,
            change_type = change_type
        )
        try:
            db.session.add(insert_data)
            db.session.add(insert_un_synced_data)
            db.session.commit()
            db.session.close()
            logging.debug(f"Complete saving data! -- type {change_type} -- running number {running_number} -- changeover {changeover}")
        except Exception as e:
            db.session.rollback()
            db.session.close() 
            logging.error(str(e))

    def cloudSyncChangeProduct(self, payload: dict):
        db.session.query(OEEProduction).filter_by(id=payload["id"]).delete()
        db.session.commit()
        db.session.close()

    def cloudSyncMachine(self, payload: dict):
        db.session.query(OEESyncData).filter_by(id=payload["id"]).delete()
        db.session.commit()
        db.session.close()

    def cloudSyncDowntime(self, payload: dict):
        db.session.query(OEEDowntime).filter_by(id=payload["id"]).delete()
        db.session.commit()
        db.session.close()

    def cloudCmdHandle(self, payload: dict):
        try:
            cmd = payload["cmd"]
            if cmd =="delete":
                logging.info(f'cmd - delete timestamp : {payload["timestamp"]}')
                time = payload["timestamp"]
                db.session.query(OEE).filter(OEE.timestamp <= time).delete()   
                db.session.query(OEESyncData).filter(OEESyncData.timestamp <= time).delete()   
                db.session.commit()
                db.session.close()
            if cmd =="get_info":
                machines = {}
                devices = db.session.query(Device).filter_by(device_type=DeviceTypes.OEE.value)
                for device in devices:
                    topic = f"/{DeviceTypes.OEE.value}/{API_VERSION}/{device.id}/raw"
                    machines[{device.id}] = redis_client.hgetall(topic)
                    logging.info("--<><>")
                send_data = {
                    "local_ip" : get_ip(),
                    "machine_count" : db.session.query(OEE).count(),
                    "machine_sync_count" : db.session.query(OEESyncData).count(),
                    "gateway_uptime" : get_uptime(),
                    "machines" : machines
                }
                db.session.close()
                MqttTopic.putToQueue(f"/{API_VERSION}/{getEnterprise()}/info", send_data)
        except Exception as e:
            logging.error(str(e))
            db.session.close()

    def cloudSettings(self, payload: dict):
        try:
            data = json.loads(payload)
            if "runningNumber" in data:
                redis_client.hset(f"/{DeviceTypes.OEE.value}/{API_VERSION}/{data['deviceId']}/raw","runningNumber", data["runningNumber"] )
        except Exception as e:
            logging.error(e)

    def clearDataStorage(self, no_commit = False):
        redis_client.delete(f"/{DeviceTypes.OEE.value}/{API_VERSION}/{self._id}/raw")
        redis_client.delete(self._production_topic)
        try:
            errors_to_delete = db.session.query(OEE).filter_by(device_id=self._id).all()
            for error in errors_to_delete:
                db.session.delete(error)
            if not no_commit:
                db.session.commit()
            logging.info(f"OEE: Success: Rows with device_id {self._id} deleted successfully!")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error: {str(e)}")

        try:
            errors_to_delete = db.session.query(OEESyncData).filter_by(device_id=self._id).all()
            for error in errors_to_delete:
                db.session.delete(error)
            if not no_commit:
                db.session.commit()
            logging.info(f"OEESyncData: Success: Rows with device_id {self._id} deleted successfully!")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error: {str(e)}")

        try:
            errors_to_delete = db.session.query(OEEDowntime).filter_by(device_id=self._id).all()
            for error in errors_to_delete:
                db.session.delete(error)
            if not no_commit:
                db.session.commit()
            logging.info(f"OEEDowntime: Success: Rows with device_id {self._id} deleted successfully!")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error: {str(e)}")

        try:
            errors_to_delete = db.session.query(OEEProduction).filter_by(device_id=self._id).all()
            for error in errors_to_delete:
                db.session.delete(error)
            if not no_commit:
                db.session.commit()
            logging.info(f"OEEProduction: Success: Rows with device_id {self._id} deleted successfully!")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error: {str(e)}")
        if not no_commit:
            db.session.close()

    def controlOverAPI(self, cmd: dict)->Tuple[bool, str]:
        return True, "control success"