from app.models.databases import db, _DEVICES_FOREIGN_KEY
from sqlalchemy import Column, Integer, String, ForeignKey

class CallBoxError(db.Model):
    __tablename__ = "call_box_error"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey(_DEVICES_FOREIGN_KEY) ,nullable=False)
    module = Column(String(50), nullable=False)
    code = Column(Integer, nullable=False)
    desc = Column(String(255), nullable=False)
    timestamp = Column(Integer)