from enum import Enum

class Template(str, Enum):
    MAIN = "main.jinja"
    MAINPARAM = "mainparam.jinja"
    PARAM = "param.jinja"
    OUTPUT = "output.jinja"
    README = "readme.md.jinja"
    AZURE_YAML = "azureyaml.jinja"
    AI_SEARCH_BICEP = "modules/aisearch/aisearch.bicep.jinja"
    AI_SEARCH_MODULE = "modules/aisearch/aisearch.module.jinja"
    AI_SERVICES_BICEP = "modules/aiservices/aiservices.bicep.jinja"
    AI_SERVICES_MODULE = "modules/aiservices/aiservices.module.jinja"
    AKS_BICEP = "modules/aks/aks.bicep.jinja"
    AKS_MODULE = "modules/aks/aks.module.jinja"
    APP_INSIGHTS_BICEP = "modules/applicationinsights/applicationinsights.bicep.jinja"
    APP_INSIGHTS_MODULE = "modules/applicationinsights/applicationinsights.module.jinja"
    APP_SERVICE_BICEP = "modules/appservice/appservice.bicep.jinja"
    APP_SERVICE_MODULE = "modules/appservice/appservice.module.jinja"
    APP_SERVICE_PLAN_BICEP = "modules/appserviceplan/appserviceplan.bicep.jinja"
    APP_SERVICE_PLAN_MODULE = "modules/appserviceplan/appserviceplan.module.jinja"
    APP_SERVICE_SETTINGS_BICEP = "modules/appservice/appservice.settings.bicep.jinja"
    APP_SERVICE_SETTINGS_MODULE = "modules/appservice/appservice.settings.module.jinja"
    BOT_SERVICE_BICEP = "modules/botservice/botservice.bicep.jinja"
    BOT_SERVICE_MODULE = "modules/botservice/botservice.module.jinja"
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
    FUNCTION_APP_SETTINGS_BICEP = "modules/functionapp/functionapp.settings.bicep.jinja"
    FUNCTION_APP_SETTINGS_MODULE = "modules/functionapp/functionapp.settings.module.jinja"
    FUNCTION_APP_PLAN_BICEP = "modules/functionappplan/functionappplan.bicep.jinja"
    FUNCTION_APP_PLAN_MODULE = "modules/functionappplan/functionappplan.module.jinja"
    KEYVAULT_BICEP = "modules/keyvault/keyvault.bicep.jinja"
    KEYVAULT_MODULE = "modules/keyvault/keyvault.module.jinja"
    LOG_ANALYTICS_BICEP = "modules/loganalytics/loganalytics.bicep.jinja"
    LOG_ANALYTICS_MODULE = "modules/loganalytics/loganalytics.module.jinja"
    OPENAI_BICEP = "modules/openai/openai.bicep.jinja"
    OPENAI_MODULE = "modules/openai/openai.module.jinja"
    POSTGRESQL_BICEP = "modules/postgresqldb/postgresqldb.bicep.jinja"
    POSTGRESQL_MODULE = "modules/postgresqldb/postgresqldb.module.jinja"
    REDIS_BICEP = "modules/redis/redis.bicep.jinja"
    REDIS_MODULE = "modules/redis/redis.module.jinja"
    RESOURCE_GROUP_BICEP = "modules/resourcegroup/resourcegroup.bicep.jinja"
    RESOURCE_GROUP_MODULE = "modules/resourcegroup/resourcegroup.module.jinja"
    SQL_DB_BICEP = "modules/sqldb/sqldb.bicep.jinja"
    SQL_DB_MODULE = "modules/sqldb/sqldb.module.jinja"
    STORAGE_ACCOUNT_BICEP = "modules/storageaccount/storageaccount.bicep.jinja"
    STORAGE_ACCOUNT_MODULE = "modules/storageaccount/storageaccount.module.jinja"
    MYSQL_BICEP = "modules/mysql/mysql.bicep.jinja"
    MYSQL_MODULE = "modules/mysql/mysql.module.jinja"
    SERVICE_BUS_BICEP = "modules/servicebus/servicebus.bicep.jinja"
    SERVICE_BUS_MODULE = "modules/servicebus/servicebus.module.jinja"
    STATIC_WEB_APP_BICEP = "modules/staticwebapp/staticwebapp.bicep.jinja"
    STATIC_WEB_APP_MODULE = "modules/staticwebapp/staticwebapp.module.jinja"
    STATIC_WEB_APP_SETTINGS_BICEP = "modules/staticwebapp/staticwebapp.settings.bicep.jinja"
    STATIC_WEB_APP_SETTINGS_MODULE = "modules/staticwebapp/staticwebapp.settings.module.jinja"
    USER_IDENTITY_BICEP = "modules/identity/useridentity.bicep.jinja"
    USER_IDENTITY_MODULE = "modules/identity/useridentity.module.jinja"
    WEBPUBSUB_BICEP = "modules/webpubsub/webpubsub.bicep.jinja"
    WEBPUBSUB_MODULE = "modules/webpubsub/webpubsub.module.jinja"
