from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.models.databases import db

#General table
class User(db.Model):
    __tablename__ = 'user'
    username = Column(String(50), primary_key=True)
    password = Column(String(50))
    enterprise = Column(String(50))
    mqtt_password = Column(String(20))
    mqtt_username = Column(String(20))
    mqtt_host = Column(String(20))
    mqtt_port = Column(Integer)

class Device(db.Model):
    __tablename__ = 'device'
    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    name = Column(String(50), primary_key=True, unique=True, nullable=False)
    device_type = Column(String(50))
    group_id = Column(String(50), ForeignKey("device_group.id") ,nullable=False)
    modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    protocol_type = Column(String(50), nullable=False)
    protocol = Column(JSON, nullable=False)
    register = Column(JSON, nullable=False)
    device = Column(JSON, nullable=False)

class DeviceGroup(db.Model):
    __tablename__ = 'device_group'
    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    name = Column(String(50), primary_key=True, unique=True, nullable=False)
    modified = Column(DateTime, default=func.now(), nullable=False)

class Log(db.Model):
    __tablename__ = 'log_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(String(50), nullable=False)
    code = Column(Integer, nullable=False)
    log_type = Column(String(50), nullable=False)
    desc = Column(String(255), nullable=False)
    date_time = Column(DateTime, default=func.now(), nullable=False)