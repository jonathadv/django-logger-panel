class LoggerPanelBaseException(Exception):
    pass


class LoggerNotFoundError(LoggerPanelBaseException):
    pass


class UnknownLoggerLevelError(LoggerPanelBaseException):
    pass


class LoggerUnknownError(LoggerPanelBaseException):
    pass
