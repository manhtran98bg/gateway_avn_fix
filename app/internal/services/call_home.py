import socket, json
import select, logging
from ..services import assignTask, BaseService
from app.internal.yaml_loader import (CALL_HOME_TOKEN, CALL_HOME_PORT, PI_SERIAL_NUMBER,
                                      CALL_HOME_FB_PORT, DEVICE_MODEL)

@assignTask('call_home_process', "Call home process")
class CallHomeProcess(BaseService):
    def _loop(self):
        __udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the server IP and port
        __udp_socket.bind(('', CALL_HOME_PORT))
        logging.info(f"UDP server is listening on port {CALL_HOME_PORT} with token {CALL_HOME_TOKEN}")
        try:
            while self.keep_run:
                # Use select to set a timeout for recvfrom
                ready, _, _ = select.select([__udp_socket], [], [], 1)  # 5-second timeout
                if ready:
                    # Receive data from the client
                    data, addr = __udp_socket.recvfrom(1024)  # 1024 is the buffer size
                    # Decode the received data (assuming it's in UTF-8)
                    received_message = data.decode('utf-8')
                    logging.debug(f"Received data from {addr}: {received_message}")
                    sendFeedback(received_message, addr[0])
                else:
                    # Handle the timeout here
                    logging.debug("Timeout - No data received within the timeout period")
        except Exception as e:
            logging.error(e)
        logging.info("Close call home process")
        __udp_socket.close()

def sendFeedback(msg: str, addr: str):
    if msg == CALL_HOME_TOKEN:
        des_port = CALL_HOME_FB_PORT
        message = {
            'model': DEVICE_MODEL,
            'serial_number': PI_SERIAL_NUMBER,
            'token': CALL_HOME_TOKEN,
        }
        message = json.dumps(message)
        logging.info(f"Call home token right. Sending feedback to {addr}!")
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(message.encode(), (addr, des_port))
        udp_socket.close()