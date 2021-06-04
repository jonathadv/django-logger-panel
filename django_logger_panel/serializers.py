from logging import Logger, getLevelName
from typing import List, Dict, Any


def log_level_serializer(level: int) -> Dict[str, Any]:
    """Receives an integer representing the Logger level and
    returns a dict with code and name representations.
    """
    return {
        "code": level,
        "name": getLevelName(level),
    }


def logger_serializer(logger: Logger) -> Dict[str, Any]:
    """Receives a Logger instance and returns a dict with
    name, level, effectiveLevel and parent values.
    """
    return {
        "name": logger.name,
        "level": log_level_serializer(logger.level),
        "effectiveLevel": log_level_serializer(logger.getEffectiveLevel()),
        "parent": logger.parent.name if logger.parent else None,
    }


def logger_list_serializer(loggers: Dict[str, Logger]) -> List[Dict[str, Any]]:
    """Receives a `List` of Logger instances and returns
    a list of dicts representing each Logger instance received.
    """
    return [logger_serializer(v) for k, v in loggers.items()]


def logger_response_serializer(log_levels: Dict[str, int], loggers: Dict[str, Logger]):
    """Receives a dict with logger levels and a list of Logger instances and returns
    a dict with the `log_levels` and `loggers` representations
    """
    data = {
        "log_levels": log_levels,
        "loggers": logger_list_serializer(loggers),
    }
    return data
