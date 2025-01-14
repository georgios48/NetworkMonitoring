"""Custom exceptions classes"""

class GeneralCustomException(Exception):
    """General custom exception class"""

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

class FailedToGetData(Exception):
    """Failed to get SNMP data"""

    def __init__(self, port, original_exception=None):
        self.port = port
        message = f"Failed to get SNMP data for port {self.port}"
        super().__init__(message)
        self.original_exception = original_exception
