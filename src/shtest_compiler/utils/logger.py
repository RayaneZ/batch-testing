
import logging
import sys
import socket
import datetime
from enum import Enum
from typing import List, Tuple

class LogType(Enum):
    PIPELINE_ERROR = "PIPELINE_ERROR"
    WARNING = "WARNING"
    ACTION = "ACTION"
    DEBUG = "DEBUG"

class RFC5424Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.utcfromtimestamp(record.created)
        if datefmt:
            # Manually handle %f for microseconds
            if "%f" in datefmt:
                s = dt.strftime(datefmt.replace("%f", "{microsecond:06d}"))
                s = s.format(microsecond=dt.microsecond)
                return s
            else:
                return dt.strftime(datefmt)
        else:
            return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    def format(self, record):
        record.hostname = socket.gethostname()
        record.asctime = self.formatTime(record, self.datefmt)
        return f"{record.asctime} {record.hostname} {record.name}[{record.process}]: [{getattr(record, 'log_type', record.levelname)}] {record.getMessage()}"

class SingletonLogger:
    """Logger singleton with RFC 5424 formatting, log storage, and export."""
    _instance = None
    _debug_enabled = False
    _log_store: List[Tuple[str, str]] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        self.logger = logging.getLogger("shtest_compiler")
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler(sys.stdout)
            formatter = RFC5424Formatter(datefmt='%Y-%m-%dT%H:%M:%S.%fZ')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _store_log(self, level: LogType, msg: str):
        self._log_store.append((level.value, str(msg)))

    def set_debug(self, enabled: bool):
        self._debug_enabled = enabled
        self._log_store = [] if enabled else self._log_store
        self.logger.setLevel(logging.DEBUG if enabled else logging.INFO)

    def is_debug_enabled(self):
        return self._debug_enabled

    def log_pipeline_error(self, msg, *args, **kwargs):
        extra = {'log_type': LogType.PIPELINE_ERROR.value}
        self.logger.error(msg, *args, extra=extra, **kwargs)
        self._store_log(LogType.PIPELINE_ERROR, msg)

    def log_warning(self, msg, *args, **kwargs):
        extra = {'log_type': LogType.WARNING.value}
        self.logger.warning(msg, *args, extra=extra, **kwargs)
        self._store_log(LogType.WARNING, msg)

    def log_action(self, msg, *args, **kwargs):
        extra = {'log_type': LogType.ACTION.value}
        self.logger.info(msg, *args, extra=extra, **kwargs)
        self._store_log(LogType.ACTION, msg)

    def debug(self, msg, *args, **kwargs):
        if self._debug_enabled:
            extra = {'log_type': LogType.DEBUG.value}
            self.logger.debug(msg, *args, extra=extra, **kwargs)
            self._store_log(LogType.DEBUG, msg)

    def export_log(self, path: str, include_levels: List[str] = None):
        with open(path, "w", encoding="utf-8") as f:
            for level, message in self._log_store:
                if include_levels is None or level in include_levels:
                    hostname = socket.gethostname()
                    import os
                    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    f.write(f"{timestamp} {hostname} shtest_compiler[{os.getpid()}]: [{level}] {message}\n")

    def reset(self):
        self._debug_enabled = False
        self._log_store = []

# Utility functions
logger = SingletonLogger()

def set_debug(enabled: bool):
    logger.set_debug(enabled)

def is_debug_enabled():
    return logger.is_debug_enabled()

def log_pipeline_error(msg, *args, **kwargs):
    logger.log_pipeline_error(msg, *args, **kwargs)

def log_warning(msg, *args, **kwargs):
    logger.log_warning(msg, *args, **kwargs)

def log_action(msg, *args, **kwargs):
    logger.log_action(msg, *args, **kwargs)

def debug_log(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)

def export_log(path: str, include_levels: List[str] = None):
    logger.export_log(path, include_levels)

def reset_logger():
    logger.reset()
