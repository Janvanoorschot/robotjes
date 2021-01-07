import os
import datetime


class TraceLog(object):

    __instance = None

    def __new__(cls, path="/data/dev/robotjes/tracelog"):
        if TraceLog.__instance is None:
            TraceLog.__instance = object.__new__(cls)
        occurance = str(to_integer(datetime.datetime.now()))
        TraceLog.__instance.__path = os.path.join(path, occurance)
        if not os.path.isdir(path):
            raise Exception(f"not a tracelog directory: {path}")
        if os.path.isdir(os.path.join(path, occurance)):
            raise Exception(f"tracelog directory already exists: {TraceLog.__instance.__path}")
        os.mkdir(TraceLog.__instance.__path)
        return TraceLog.__instance

    def trace(self, type, *args):
        filename = os.path.join(self.__path, f"{type}.log")
        with open(filename, "a") as f:
            line = str(to_integer(datetime.datetime.now())) + ',' + ','.join([str(x) for x in args]) + '\n'
            f.write(line)


    @staticmethod
    def default_logger():
        return TraceLog()


def to_integer(dt_time: datetime.datetime):
    return dt_time.hour*10000+dt_time.minute*100 + dt_time.second



