import logging
from app.internal.services import assignTask, BaseService
from app import db
from app.models.databases import (CallBoxError, getEnterprise, Device)
from app.dependencies.type_define import DeviceTypes, LogType
from app.internal.yaml_loader import API_VERSION, SENDING_RATE
from app.dependencies.mqtt_utils import MqttTopic
from app.internal.yaml_loader import PI_SERIAL_NUMBER

@assignTask('sync_error', 'Synchronize Error Of Call Box')
class CallBoxErrorService(BaseService):
    def _loop(self):
        logging.info("--start sync error")
        while self.keep_run:
            self.wait(SENDING_RATE)
            call_boxes = db.session.query(Device).filter_by(device_type=DeviceTypes.CALL_BOX.value)
            no_update = True
            try:
                for call_box in call_boxes:
                    result = db.session.query(CallBoxError).filter_by(device_id=call_box.id).order_by(CallBoxError.id.asc()).first()
                    if not result:
                        continue
                    no_update = False
                    send_data = {
                        "id" : result.id,
                        "type": LogType.ERROR.value,
                        "deviceId" : result.device_id,
                        "module" : result.module,
                        "timestamp" : result.timestamp,
                        "code" : result.code,
                        "desc" : result.desc,
                        "gateway_id": PI_SERIAL_NUMBER
                    }
                    MqttTopic.putToQueue(f"/{API_VERSION}/{getEnterprise()}/machine", send_data)
                    logging.debug(f"sending ->> errors log {send_data['desc']}")
                if call_boxes.count() == 0 and no_update:
                    self.wait(10.)
                db.session.close()
            except Exception as e:
                logging.error(e)