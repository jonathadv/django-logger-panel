"""
Core module for Django Logger Panel
"""

from logging import Logger, PlaceHolder, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from typing import Dict
from .exceptions import LoggerPanelNotFoundError, LoggerPanelUnknownError

__all__ = [
    "LEVELS",
    "ALL_LOG_LEVEL",
    "set_logger_level",
    "get_all_loggers",
    "get_all_log_level",
]

LEVELS = {
    "CRITICAL": CRITICAL,
    "ERROR": ERROR,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}

ALL_LOG_LEVEL = NOTSET


def set_logger_level(log_name: str, log_level: str):
    """
    :param log_level: the logger name as defined in `logging.getLogger(<name>)`
    :type log_level: str
    :param log_level: the name of the log level to be set
    :type log_name: str
    """
    loggers = get_all_loggers()

    try:
        if log_name == "ALL":
            # pylint: disable=global-statement
            global ALL_LOG_LEVEL
            ALL_LOG_LEVEL = LEVELS.get(log_level, NOTSET)
            for _, logger in loggers.items():
                logger.setLevel(log_level)
        else:
            loggers.get(log_name).setLevel(log_level)
    except (KeyError, AttributeError) as err:
        raise LoggerPanelNotFoundError(f"Logger '{log_name}' not found") from err
    except Exception as err:
        raise LoggerPanelUnknownError(
            f"A unknown error happened while setting logger '{log_name}'"
        ) from err


def get_all_loggers() -> Dict[str, Logger]:
    """
    :return: a dictionary of logger objects
    :rtype: Dict[str, Logger]
    """
    loggers = {
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


def get_all_log_level() -> int:
    """
    :return: the value of `ALL_LOG_LEVEL`
    :rtype: int
    """
    return ALL_LOG_LEVEL
