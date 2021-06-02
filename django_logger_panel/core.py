"""
Core module for Django Logger Panel
"""

from logging import Logger, PlaceHolder, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from typing import Dict
from .exceptions import LoggerNotFoundError, LoggerUnknownError, UnknownLoggerLevelError

__all__ = [
    "LEVELS",
    "set_logger_level",
    "get_all_loggers",
]

LEVELS = {
    "CRITICAL": CRITICAL,
    "ERROR": ERROR,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}


class AllLogger:
    """
    A stub of Logger class to track the global "_all_loggers_" level
    """

    def __init__(self):
        self.name = "_all_loggers_"
        self.level = NOTSET
        self.parent = None

    # pylint: disable=invalid-name
    def setLevel(self, level):
        """Sets log level"""
        if isinstance(level, int):
            self.level = level
        else:
            self.level = LEVELS[level]

    # pylint: disable=invalid-name
    def getEffectiveLevel(self):
        """Mimics the getEffectiveLevel() from a real Logger"""
        return self.level


ALL_LOGGER = AllLogger()


def set_logger_level(log_name: str, log_level: str):
    """
    :param log_level: the logger name as defined in `logging.getLogger(<name>)`
    :type log_level: str
    :param log_level: the name of the log level to be set
    :type log_name: str
    """
    loggers = get_all_loggers()

    try:
        if log_name == ALL_LOGGER.name:
            for _, logger in loggers.items():
                logger.setLevel(log_level)
        else:
            loggers.get(log_name).setLevel(log_level)
    except (KeyError, AttributeError) as err:
        raise LoggerNotFoundError(f"Logger '{log_name}' not found") from err
    except ValueError as err:
        raise UnknownLoggerLevelError(err) from err
    except Exception as err:
        raise LoggerUnknownError(err) from err


def get_all_loggers() -> Dict[str, Logger]:
    """
    :return: a dictionary of logger objects
    :rtype: Dict[str, Logger]
    """
    loggers = {
        ALL_LOGGER.name: ALL_LOGGER,
        "root": Logger.root,
    }
    loggers.update(
        {
            key: logger
            for key, logger in Logger.manager.loggerDict.items()
            if not isinstance(logger, PlaceHolder)
        }
    )
    return loggers
