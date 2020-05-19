from . import Base
from sqlalchemy import Column, Integer, String, DateTime, Float

class ResponseTime(Base):
    __tablename__ = 'responsetime'
    id = Column(Integer, primary_key=True)
    host = Column(String)
    timestamp = Column(DateTime)
    funname = Column(String)
    count = Column(Integer)
    cummulated = Column(Float)

