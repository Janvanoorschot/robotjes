from . import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger

class ResponseTime(Base):
    __tablename__ = 'responsetime'
    id = Column(Integer, primary_key=True)
    host = Column(String)
    process = Column(BigInteger)
    thread = Column(BigInteger)
    timestamp = Column(DateTime)
    funname = Column(String)
    count = Column(Integer)
    cummulated = Column(Float)

