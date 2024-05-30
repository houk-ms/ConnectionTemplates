from enum import Enum


class Abbreviation(str, Enum):
    AI_SEARCH = "ais"
    AI_SERVICES = "aisvc"
    APPLICATION_INSIGHTS = "ai"
    APP_SERVICE = "app"
    APP_SERVICE_PLAN = "plan"
    BOT_SERVICE = "bot"
    CONTAINER_APP = "aca"
    CONTAINER_APP_ENV = "env"
    CONTAINER_REGISTRY = "acr"
    COSMOS_DB = 'cosmos'
    FUNCTION_APP = "func"
    KEYVAULT = "kv"
    KEYVAULT_SECRET = "secret"
    MYSQL_DB = "mysql"
    OPENAI = "openai"
    POSTGRESQL_DB = "psql"
    REDIS_CACHE = "redis"
    RESOURCE_GROUP = "rg"
    SQL_DB = "sql"
    STORAGE_ACCOUNT = "strg"
    STATIC_WEB_APP = "swa"
    SERVICE_BUS = "sb"
    USER_IDENTITY = "umi"
    WEB_PUBSUB = "wps"
