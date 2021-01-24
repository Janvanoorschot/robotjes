from . import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger

class LogMessage(Base):
    __tablename__ = 'logmessage'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    host = Column(String)
    process = Column(BigInteger)
    thread = Column(BigInteger)
    filename = Column(String)
    lineno = Column(Integer)
    levelname = Column(String)
    message = Column(String)
