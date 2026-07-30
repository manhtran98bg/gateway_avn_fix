from app.models.databases import db, _DEVICES_FOREIGN_KEY
from sqlalchemy import Column, Integer, String, ForeignKey

class OEE(db.Model):
    __tablename__ = "oee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey(_DEVICES_FOREIGN_KEY) ,nullable=False)
    machine_status = Column(Integer, nullable=False)
    actual = Column(Integer, nullable=False)
    running_number = Column(Integer, nullable=False)
    timestamp = Column(Integer)
    changeover = Column(Integer)
    up_time = Column(Integer)
    change_type = Column(Integer)

class OEEProduction(db.Model):
    __tablename__ = "oee_production"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey(_DEVICES_FOREIGN_KEY), nullable=False)
    start_time = Column(Integer, nullable=False)
    start_production_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    actual = Column(Integer)
    running_number = Column(Integer, nullable=False)

class OEEDowntime(db.Model):
    __tablename__ = "oee_downtime"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey(_DEVICES_FOREIGN_KEY), nullable=False)
    machine_status = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    running_number = Column(Integer, nullable=False)

class OEESyncData(db.Model):
    __tablename__ = "oee_sync"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey(_DEVICES_FOREIGN_KEY), nullable=False)
    machine_status = Column(Integer, nullable=False)
    actual = Column(Integer, nullable=False)
    running_number = Column(Integer, nullable=False)
    timestamp = Column(Integer)
    changeover = Column(Integer)
    up_time = Column(Integer)
    change_type = Column(Integer)