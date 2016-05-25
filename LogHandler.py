import logging


class LogHandler(logging.Handler):
    def __init__(self, view):
        logging.Handler.__init__(self)
        self.view = view
        self.view.logBrowser.append('LogHandler initiated!')

    def emit(self, record):
        self.view.logBrowser.append(record.message)

