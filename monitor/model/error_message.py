from . import Base
from sqlalchemy import Column, Integer, String, DateTime, Float

class ErrorMessage(Base):
    __tablename__ = 'errormessage'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    type = Column(String)
    message = Column(String)

