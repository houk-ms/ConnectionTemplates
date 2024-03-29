from enum import Enum

class Template(str, Enum):
    MAIN = "main.jinja"	
    PARAM = "param.jinja"
    OUTPUT = "output.jinja"
    APP_INSIGHTS_BICEP = "modules/applicationinsights/applicationinsights.bicep.jinja"
    APP_INSIGHTS_MODULE = "modules/applicationinsights/applicationinsights.module.jinja"
    APP_SERVICE_BICEP = "modules/appservice/appservice.bicep.jinja"
    APP_SERVICE_MODULE = "modules/appservice/appservice.module.jinja"
    APP_SERVICE_PLAN_BICEP = "modules/appserviceplan/appserviceplan.bicep.jinja"
    APP_SERVICE_PLAN_MODULE = "modules/appserviceplan/appserviceplan.module.jinja"
    APP_SERVICE_SETTINGS_BICEP = "modules/appservice/appservice.settings.bicep.jinja"
    APP_SERVICE_SETTINGS_MODULE = "modules/appservice/appservice.settings.module.jinja"
    CONTAINER_APP_BICEP = "modules/containerapp/containerapp.bicep.jinja"
    CONTAINER_APP_MODULE = "modules/containerapp/containerapp.module.jinja"
    CONTAINER_APP_ENV_BICEP = "modules/containerappenv/containerappenv.bicep.jinja"
    CONTAINER_APP_ENV_MODULE = "modules/containerappenv/containerappenv.module.jinja"
    CONTAINER_REGISTRY_BICEP = "modules/containerregistry/containerregistry.bicep.jinja"
    CONTAINER_REGISTRY_MODULE = "modules/containerregistry/containerregistry.module.jinja"
    COSMOS_DB_BICEP = "modules/cosmosdb/cosmosdb.bicep.jinja"
    COSMOS_DB_MODULE = "modules/cosmosdb/cosmosdb.module.jinja"
    FUNCTION_APP_BICEP = "modules/functionapp/functionapp.bicep.jinja"
    FUNCTION_APP_MODULE = "modules/functionapp/functionapp.module.jinja"
    KEYVAULT_BICEP = "modules/keyvault/keyvault.bicep.jinja"
    KEYVAULT_MODULE = "modules/keyvault/keyvault.module.jinja"
    LOG_ANALYTICS_BICEP = "modules/loganalytics/loganalytics.bicep.jinja"
    LOG_ANALYTICS_MODULE = "modules/loganalytics/loganalytics.module.jinja"
    POSTGRESQL_BICEP = "modules/postgresqldb/postgresqldb.bicep.jinja"
    POSTGRESQL_MODULE = "modules/postgresqldb/postgresqldb.module.jinja"
    REDIS_BICEP = "modules/redis/redis.bicep.jinja"
    REDIS_MODULE = "modules/redis/redis.module.jinja"
    SQL_DB_BICEP = "modules/sqldb/sqldb.bicep.jinja"
    SQL_DB_MODULE = "modules/sqldb/sqldb.module.jinja"
    STORAGE_ACCOUNT_BICEP = "modules/storageaccount/storageaccount.bicep.jinja"
    STORAGE_ACCOUNT_MODULE = "modules/storageaccount/storageaccount.module.jinja"