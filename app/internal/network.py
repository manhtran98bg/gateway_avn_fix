import subprocess
import subprocess, re
import logging, pywifi
from typing import List, Union, Tuple, Optional
import pywifi.const

# Disable or set a higher log level for pywifi and its related libraries
logging.getLogger("pywifi").setLevel(logging.ERROR)
logging.getLogger("pywifi.pywifi").setLevel(logging.ERROR)
logging.getLogger("pywifi.getwifi").setLevel(logging.ERROR)
from app.internal.yaml_loader import ETH, WIFI

def getWifiSSID()->Optional[str]:
    try:
        result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)

        if result.returncode == 0:
            ssid = result.stdout.strip()
            return ssid
        else:
            return None
    except Exception as e:
        logging(e)
        return None

def isDHCPEnabledForWifi(ssid)->bool:
    try:
        with open(f'/etc/NetworkManager/system-connections/{ssid}.nmconnection', 'r') as f:
            data = f.read()
        lines = data.split('\n')
        for line in lines:
            data = line.split('=')
            if data[0] == 'method':
                return (data[1] == 'auto')
        return False
    except Exception as e:
        logging.error(e)
        return False
    
def isDHCPEnabled()->bool:
    nmcli = "nmcli connection show"
    connection_name = "Wired connection 1"
    command = f"{nmcli} '{connection_name}'"
    output = subprocess.check_output(command, shell=True, text=True)
    lines = output.split('\n')
    try:
        for line in lines:
            value = line.split(' ')
            if value[0] == "ipv4.method:":
                return (value[-1] == 'auto')
        return False
    except Exception as e:
        logging.error(e)

def getWifiSignalStrength(interface)->Optional[int]:
    try:
        result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)

        if result.returncode == 0:
            signal_level_match = re.search(r"Signal level=(-\d+)", result.stdout)
            if signal_level_match:
                signal_level = signal_level_match.group(1)
                return signal_level

        return None
    except Exception as e:
        logging.error(e)
        return None

def getEthernetPort(interface: str, network: dict)->Optional[dict]:
        network_data = {
            'type': 'unknown',
            'mac': None,
            'ip': None,
            'subnet_mask': None,
            'dhcp': None,
            'ssid': None,
            'signal': None,
            'enable': False
        }
        network_data.update(network)
        if interface == 'lo':
            return None
        if interface == ETH:
            network_data['type'] = "ethernet"
        elif interface == WIFI:
            network_data['type'] = "wifi"
        elif 'en' in interface:
            network_data['type'] = 'ethernet'
        else:
            network_data['type'] = 'wifi'

        if network_data['type'] == 'wifi' and getWifiSignalStrength(interface) != None:
            network_data['ssid'] = getWifiSSID()
            network_data['signal'] = getWifiSignalStrength(interface)

        if network_data['enable'] and network_data['ssid'] != None:
                network_data['dhcp'] = isDHCPEnabledForWifi(network_data['ssid'])
        elif network_data['type'] == "ethernet":
            network_data['dhcp'] = isDHCPEnabled()
        return network_data


def getNetworkInterfaceAddrs():
    result_ifconfig = subprocess.run(['ifconfig'], capture_output=True, text=True)
    result_route = subprocess.run(['route', '-n'], capture_output=True, text=True)

    if result_ifconfig.returncode == 0 and result_route.returncode == 0:
        interfaces = {}
        current_interface = None  # Initialize here

        for line in result_ifconfig.stdout.split('\n'):
            if len(line.strip().split(':')) == 2:
                current_interface = line.split(':')[0].strip()
                interfaces[current_interface] = {
                    'enable': False,
                    'ip': None,
                    'subnet_mask': None,
                    'mac': None,
                    'gateway': None  # Initialize gateway here
                }
            elif current_interface != 'lo' and 'inet ' in line.strip():
                value = line.strip().split(' ')
                new_value = {
                    'ip': value[1],
                    'subnet_mask': value[4],
                    'enable': True
                }
                interfaces[current_interface].update(new_value)

        for line in result_route.stdout.split('\n'):
            if 'UG' in line:
                gateway_ip = line.split()[1]
                interfaces[current_interface]['gateway'] = gateway_ip

        if 'lo' in interfaces:
            del interfaces['lo']
        return interfaces
    else:
        return []

def getNetworkInfo()->List[dict]:
    network_info = []
    networks = getNetworkInterfaceAddrs()
    for interface in networks:
        if interface not in [ETH, WIFI]:
            continue
        network_data = getEthernetPort(interface, networks[interface])
        if isinstance(network_data, dict):
            network_info.append(network_data)

    return network_info

def isIpv4Address(ip_address):
    ipv4_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return bool(re.match(ipv4_pattern, ip_address))

def isNetMask(netmask: str)->Tuple[bool, Union[str, int, None]]:
    if isIpv4Address(netmask):
        return (True, netmask)
    try:
        mask = int(netmask)
        if mask >= 2 and mask <= 253:
            return (True, mask)
    except Exception as e:
        logging.error(e)
    return (False, None)

def updateDHCPForEthernet(network: dict)->bool:
    pass

def updateStaticEthernet(network: dict)->bool:
    pass

def updateEthernet(network: dict)->bool:
    pass

def updateDHCPForWifi(network: dict)->bool:
    pass

def updateStaticWifi(network: dict)->bool:
    ip = network.get('static_ip')
    netmask = network.get('static_subnet_mask')
    gateway = network.get('static_gateway')
    (is_mask, netmask) = isNetMask(netmask)
    if not isIpv4Address(ip) and not is_mask:
        return False
    # is_gateway = isIpv4Address(gateway)

def updateWifi(network: dict)->bool:
    required_list = ['ssid', 'password', 'dhcp']
    for arg in required_list:
        if network.get(arg) == None:
            return False
    if network.get('dhcp'):
        return updateDHCPForWifi(network)
    else:
        return updateStaticWifi(network)

def listWifiNetworks()->List[dict]:
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    scan_results = iface.scan_results()
    wifi_list = []
    for network in scan_results:
        wifi = {
            "SSID": network.ssid,
            "signal": network.signal
        }
        wifi_list.append(wifi)
    return wifi_list