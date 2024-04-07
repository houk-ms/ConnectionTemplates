from enum import Enum

class Abbreviation(str, Enum):
    APPLICATION_INSIGHTS = "ai"
    APP_SERVICE = "app"
    APP_SERVICE_PLAN = "appplan"
    CONTAINER_APP = "aca"
    CONTAINER_APP_ENV = "env"
    CONTAINER_REGISTRY = "acr"
    COSMOS_DB = 'cosmos'
    POSTGRESQL_DB = "psql"
    REDIS_CACHE = "redis"
    RESOURCE_GROUP = "rg"
    SQL_DB = "sql"
    STORAGE_ACCOUNT = "st"
    KEYVAULT = "kv"
    KEYVAULT_SECRET = "kvsec"
    MYSQL_DB = "mysql-"