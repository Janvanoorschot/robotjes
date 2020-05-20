from . import Base
from sqlalchemy import Column, Integer, String, DateTime, Float

class LogMessage(Base):
    __tablename__ = 'logmessage'
    id = Column(Integer, primary_key=True)
    host = Column(String)
    timestamp = Column(DateTime)
    message = Column(String)
    filename = Column(String)
    lineno = Column(Integer)
    levelname = Column(String)

