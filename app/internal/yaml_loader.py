import yaml, logging, coloredlogs
from app import APP_PATH
from typing import Tuple, Dict, List
from datetime import datetime

def yamlFileLoader(file_name: str)->dict:
    try:
        with open(file_name, 'r') as yaml_file:
            yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return yaml_data
    except Exception as e:
        logging.error(e)
        return {}
__YAML_DIR = f'{APP_PATH}/config'

def _loadSoftwareVersion()->Tuple[str, str, str, str]:
    yaml_data = yamlFileLoader(f'{__YAML_DIR}/software_version.yaml')
    major = 0
    minor = 0
    path = 0
    author = ""
    email = ""
    api_version = ""
    if "software_version" in yaml_data:
        software_data = yaml_data["software_version"]
        major = software_data["major"] if "major" in software_data else major
        minor = software_data["minor"] if "minor" in software_data else minor
        path = software_data["path"] if "path" in software_data else path
    author = yaml_data["author"] if "author" in yaml_data else author
    email = yaml_data["email"] if "email" in yaml_data else email
    api_version = yaml_data["api_version"] if "email" in yaml_data else email
    software = f'v.{major}.{minor}.{path}'
    return (software, api_version, author, email)

(SOFTWARE_VER, API_VERSION, AUTHOR, EMAIL) = _loadSoftwareVersion()

def _loadDatabaseConfigure()->Tuple[str, str]:
    yaml_data = yamlFileLoader(f'{__YAML_DIR}/database_config.yaml')
    host = ""
    port = 0
    username = ""
    password = ""
    database_name = ""
    if "database" in yaml_data:
        yaml_data = yaml_data["database"]
        username = yaml_data["username"] if "username" in yaml_data else username
        password = yaml_data["password"] if "password" in yaml_data else password
        host = yaml_data["host"] if "host" in yaml_data else host
        port = yaml_data["port"] if "port" in yaml_data else port
        database_name = yaml_data["database_name"] if "database_name" in yaml_data else database_name
        limit_record = yaml_data["limit_record"] if "limit_record" in yaml_data else 1000
    db_url = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
    mariadb = f'mysql+pymysql://{username}:{password}@{host}:{port}'
    return (db_url, mariadb, database_name, limit_record)
(DATABASE_URL, MARIADB_URL, DATABASE_NAME, LIMIT_RECORD) = _loadDatabaseConfigure()

def _loadLoggingConfigure()->Tuple[str, str]:
    yaml_data = yamlFileLoader(f'{__YAML_DIR}/logging.yaml')
    fmt = '[%(hostname)s] [%(filename)s:%(lineno)s - %(funcName)s() ] %(asctime)s %(levelname)s %(message)s'
    level = 'infor'
    limit_logger_file = 7
    download_logger_token = 'rostek@2019#'
    fmt = yaml_data["fmt"] if "fmt" in yaml_data else fmt
    level = yaml_data["level"] if "level" in yaml_data else level
    limit_logger_file = (yaml_data["limit_logger_file"] 
        if "limit_logger_file" in yaml_data else limit_logger_file)
    download_logger_token = (yaml_data["download_logger_token"] 
        if "download_logger_token" in yaml_data else download_logger_token)
    return (level, fmt, limit_logger_file, download_logger_token)
(LOGGING_LEVEL, _FMT, LIMIT_LOGGER, DOWNLOAD_LOGGER_TOKEN) = _loadLoggingConfigure()

current_date = datetime.now().strftime('%y_%m_%d')
file_handler = logging.FileHandler(f'{APP_PATH}/resource/logging/{current_date}.log')
file_formatter = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)s() ] %(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logging.getLogger().addHandler(file_handler)
coloredlogs.install(level=LOGGING_LEVEL, fmt = _FMT)

def _loadComConfig()->Dict[str, str]:
    yaml_data = yamlFileLoader(f'{__YAML_DIR}/com.yaml')
    com_dict = {}
    for data in yaml_data:
        name = data['name'] if 'name' in data else None
        port = data['port'] if 'port' in data else None
        if name != None and port != None:
            com_dict[name] = port
    return com_dict
COM_DICT = _loadComConfig()

def _loadCallHomeConfig()->Tuple[str, int]:
    yaml_data = yamlFileLoader(f'{__YAML_DIR}/callhome.yaml')
    port = yaml_data["server_port"] if "server_port" in yaml_data else 13526
    token = yaml_data["callhome_token"] if "callhome_token" in yaml_data else None
    fb_port = yaml_data["feedback_port"] if "feedback_port" in yaml_data else 15758
    device_model = yaml_data["device_model"] if "device_model" in yaml_data else "gateway"
    return (token, device_model, port, fb_port)

(CALL_HOME_TOKEN, DEVICE_MODEL, CALL_HOME_PORT, CALL_HOME_FB_PORT) = _loadCallHomeConfig()

def _loadFactorySetting()->Tuple[str, str, str, str, str]:
    data = yamlFileLoader(f'{__YAML_DIR}/factory_setting.yaml')
    return (data['user']['username'], data['user']['password'],
            data['user']['enterprise'], data['device_group'],
            data.get('gateway_id', ''))
(DEFAULT_USER, DEFAULT_PWD, DEFAULT_ETP, GROUP, GATEWAY_ID) = _loadFactorySetting()

def getSerialNumber()->str:
    if GATEWAY_ID:
        return GATEWAY_ID
    try:
        with open('/proc/cpuinfo', 'r') as file:
            for line in file:
                if line.startswith('Serial'):
                    serial_number = line.split(':')[1].strip()
                    return serial_number
        return "serial_invalid"
    except FileNotFoundError:
        return "serial_invalid"
    
PI_SERIAL_NUMBER = getSerialNumber()

def getRedis()->Tuple[str, int, str, List[Dict[str, str]]]:
    data = yamlFileLoader(f'{__YAML_DIR}/redis.yaml')
    return (data['host'], data['port'],
            data['password'], data['topic_prefix'])

(REDIS_HOST, REDIS_PORT, REDIS_PWD, REDIS_TOPICS) = getRedis()

def getMqtt()->Tuple[int, int]:
    data = yamlFileLoader(f'{__YAML_DIR}/mqtt.yaml')
    return (data['maximum_send_failed'], data['default_port'])

(MAXIMUM_SEND_FAILED, DEFAULT_PORT) = getMqtt()

def getOEEConfig()->float:
    return yamlFileLoader(f'{__YAML_DIR}/oee.yaml')['sending_rate']

SENDING_RATE = getOEEConfig()

def loadNetwork()->Tuple[str, str]:
    data = yamlFileLoader(f'{__YAML_DIR}/network.yaml')
    return data["wifi"], data["eth"]

WIFI, ETH = loadNetwork()
