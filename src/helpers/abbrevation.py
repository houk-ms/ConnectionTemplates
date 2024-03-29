from enum import Enum

class Abbreviation(str, Enum):
    APPLICATION_INSIGHTS = "ai-"
    APP_SERVICE = "app-"
    APP_SERVICE_PLAN = "plan-"
    CONTAINER_APP = "aca-"
    CONTAINER_APP_ENV = "env_"
    CONTAINER_REGISTRY = "acr-"
    COSMOS_DB = 'cosmos_'
    POSTGRESQL_DB = "psql-"
    REDIS_CACHE = "redis-"
    RESOURCE_GROUP = "rg-"
    SQL_DB = "sql-"
    STORAGE_ACCOUNT = "st"
    KEYVAULT = "kv"
    FUNCTIOM_APP = "func-"