import logging
from app.internal.services import assignTask, BaseService
from app import db
from app.models.databases import (OEESyncData, getEnterprise, 
                                  OEEDowntime, Device, OEEProduction)
from app.dependencies.type_define import DeviceTypes
from app.internal.yaml_loader import API_VERSION, SENDING_RATE
from app.dependencies.mqtt_utils import MqttTopic

@assignTask('synch oee data', 'Synchronize Data process')
class SyncOEEData(BaseService):
    def _loop(self):
        logging.info("--start sync data")
        global SENDING_RATE
        while self.keep_run:
            self.wait(SENDING_RATE)
            oee_devices = db.session.query(Device).filter_by(device_type=DeviceTypes.OEE.value)
            no_update = True
            try:
                for oee in oee_devices:
                    result = db.session.query(OEESyncData).filter_by(device_id=oee.id).order_by(OEESyncData.id.asc()).first()
                    if not result:
                        continue
                    no_update = False
                    send_data = {
                        "id" : result.id,
                        "deviceId" : result.device_id,
                        "runningNumber" : result.running_number,
                        "timestamp" : result.timestamp,
                        "actual" : result.actual,
                        "machineStatus" : result.machine_status,
                        "upTime" : result.up_time,
                        "changeover" : result.changeover,
                        "changeType" : result.change_type
                    }
                    MqttTopic.putToQueue(f"/{API_VERSION}/{getEnterprise()}/machine", send_data)
                    logging.debug(f"Complete sending ->> actual {send_data['actual']}")
                if oee_devices.count() == 0 and no_update:
                    self.wait(10.)
                db.session.close()
            except Exception as e:
                logging.error(e)

@assignTask('synch oee production data', 'Synchronize Production Data process')
class SyncOEEProductionData(BaseService):
    def _loop(self):
        logging.info("--start sync production")
        global SENDING_RATE
        while self.keep_run:
            self.wait(SENDING_RATE)
            oee_devices = db.session.query(Device).filter_by(device_type=DeviceTypes.OEE.value)
            no_update = True
            try:
                for oee in oee_devices:
                    result = db.session.query(OEEProduction).filter_by(device_id=oee.id).order_by(OEEProduction.id.asc()).first()
                    if not result:
                        continue
                    no_update = False
                    send_data = {
                        "id" : result.id,
                        "deviceId" : result.device_id,
                        "start_time" : result.start_time,
                        "start_production_time" : result.start_production_time,
                        "end_time" : result.end_time,
                        "actual" : result.actual,
                        "runningNumber" : result.running_number
                    }
                    MqttTopic.putToQueue(f"/{API_VERSION}/{getEnterprise()}/production", send_data)
                    logging.debug(f"Complete sending ->> actual {send_data['actual']}")
                if oee_devices.count() == 0 and no_update:
                    self.wait(10.)
                db.session.close()
            except Exception as e:
                logging.error(e)

@assignTask('synch oee down time data', 'Synchronize Down Time Data process')
class SyncOEEDownTimeData(BaseService):
    def _loop(self):
        logging.info("--start sync downtime")
        global SENDING_RATE
        while self.keep_run:
            self.wait(SENDING_RATE)
            oee_devices = db.session.query(Device).filter_by(device_type=DeviceTypes.OEE.value)
            no_update = True
            try:
                for oee in oee_devices:
                    result = db.session.query(OEEDowntime).filter_by(device_id=oee.id).order_by(OEEDowntime.id.asc()).first()
                    if not result:
                        continue
                    no_update = False
                    send_data = {
                        "id" : result.id,
                        "device_id" : result.device_id,
                        "timestamp" : result.timestamp,
                        "duration" : result.duration,
                        "status" : result.machine_status,
                        "reason_code" : 0,
                        "runningNumber" : result.running_number
                    }
                    MqttTopic.putToQueue(f"/{API_VERSION}/{getEnterprise()}/downtime", send_data)
                    logging.debug(f"Complete sending ->> downtime {send_data['status']}")
                if oee_devices.count() == 0 and no_update:
                    self.wait(10.)
                db.session.close()
            except Exception as e:
                logging.error(e)