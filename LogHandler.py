import logging
from datetime import datetime
logging.StreamHandler()

class LogHandler(logging.Handler):
    def __init__(self, view):
        logging.Handler.__init__(self)
        self.view = view

    def emit(self, record):
        # print(record.name)
        # print(record.msecs)
        # print(record.levelname)
        # print(record.pathname)
        # print(record.lineno)
        # print(record.msg)
        # print(record.args)
        # print(record.exc_info)
        # print(record.getMessage())
        now = datetime.now()
        message = "[{level}] {time} - {msg}".format(time=str(now), level=record.levelname, msg=record.msg)

        self.view.logBrowser.append(message)
