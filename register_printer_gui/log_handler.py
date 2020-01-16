import logging
from PySide2.QtCore import (
    QObject,
    Signal)

class Signaller(QObject):
    signal = Signal(str)

class LogHandler(logging.Handler):
    def __init__(self, slot_func):
        super().__init__()
        self.slot_func = slot_func
        self.log = Signaller()
        self.log.signal.connect(slot_func)
        return

    def emit(self, record):
        message = self.format(record)
        self.log.signal.emit(message)
        return

