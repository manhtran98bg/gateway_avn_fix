from app import DATABASE_URL, app
from sqlalchemy_utils import create_database, database_exists
from flask_sqlalchemy import SQLAlchemy
from app.internal.yaml_loader import (DEFAULT_USER, DEFAULT_PWD, DEFAULT_ETP, GROUP)
from uuid import uuid4

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app=app)
_DEVICES_FOREIGN_KEY = 'device.id'
from .gateway_db import (User, Device, 
                         DeviceGroup, Log)
from .oee import (OEE, OEEProduction, OEEDowntime,
                  OEESyncData)
from .callbox import CallBoxError
ENTERPRISE = None

def setEnterprise(value: str):
    global ENTERPRISE
    if isinstance(value, str):
        ENTERPRISE = value
    else:
        raise ValueError("Enterprise need is int")

def getEnterprise()->str:
    global ENTERPRISE
    return ENTERPRISE    

db.create_all()
def setupDB(clear_table: bool = False):
    if clear_table:
        for table_name in db.engine.table_names():
            table = db.Model.metadata.tables[table_name]
            db.session.execute(table.delete())
        db.session.commit()
    default_user = db.session.query(User).filter_by(username=DEFAULT_USER).first()
    init_db = not default_user
    if init_db:
        setEnterprise(DEFAULT_ETP)
        default_user = User(username=DEFAULT_USER, password=DEFAULT_PWD, enterprise=DEFAULT_ETP)  # Assuming 'enterprise' can be None
        # Add the default user to the database session
        db.session.add(default_user)
        db.session.commit()
    else:
        setEnterprise(default_user.enterprise)
    if init_db:
        default_groups = DeviceGroup(id=str(uuid4()), name=GROUP)  # Assuming 'enterprise' can be None
        # Add the default user to the database session
        db.session.add(default_groups)
        db.session.commit()
    db.session.close()
setupDB()
TABLE_LIST = (User, Device, DeviceGroup, Log, CallBoxError,
              OEE, OEEProduction, OEEDowntime, OEESyncData)

