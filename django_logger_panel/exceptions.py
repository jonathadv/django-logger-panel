class LoggerPanelBaseException(Exception):
    pass


class LoggerPanelNotFoundError(LoggerPanelBaseException):
    pass


class LoggerPanelUnknownError(LoggerPanelBaseException):
    pass
