import socket
from datetime import timedelta

def get_ip()->str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 5))
    ipv4 = s.getsockname()[0]
    s.close()
    return ipv4


def get_uptime()->str:
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return str(timedelta(seconds = round(uptime_seconds)))