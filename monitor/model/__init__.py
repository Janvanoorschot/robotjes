from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .response_times import ResponseTime
from .error_message import  ErrorMessage
from .log_message import  LogMessage
