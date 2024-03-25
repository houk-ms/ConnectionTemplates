from enum import Enum

class Abbreviation(str, Enum):
    APP_SERVICE = "app-"
    APP_SERVICE_PLAN = "plan-"
    CONTAINER_APP = "aca-"
    CONTAINER_APP_ENV = "env_"
    CONTAINER_REGISTRY = "acr-"
    STORAGE_ACCOUNT = "st"
    KEYVAULT = "kv"