from enum import Enum

class ConnectionType(str, Enum):
    HTTP = 'http'
    SECRET = 'secret'
    SYSTEMIDENTITY = 'system-identity'