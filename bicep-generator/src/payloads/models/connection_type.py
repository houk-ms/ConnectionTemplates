from enum import Enum

class ConnectionType(str, Enum):
    """ConnectionType is a string enum that represents the type of a resource binding."""
    HTTP = 'http'
    SECRET = 'secret'
    SYSTEMIDENTITY = 'system-identity'