from enum import Enum


class Template(str, Enum):
    MAIN = "main.tf.jinja"	
    VARIABLE = "variable.tf.jinja"
    OUTPUT = "output.tf.jinja"
    BLOCKS = "blocks.tf.jinja"
    APP_INSIGHTS_TF = "modules/applicationinsights/applicationinsights.tf.jinja"
    APP_SERVICE_LINUX_TF = "modules/appservice/appservicelinux.tf.jinja"
    APP_SERVICE_PLAN_TF = "modules/appserviceplan/appserviceplan.tf.jinja"
    APP_SERVICE_SETTINGS_TF = "modules/appservice/appservice.settings.tf.jinja"
    BOT_SERVICE_TF = "modules/botservice/botservice.tf.jinja"
    CONTAINER_APP_TF = "modules/containerapp/containerapp.tf.jinja"
    CONTAINER_APP_ENV_TF = "modules/containerappenv/containerappenv.tf.jinja"
    CONTAINER_REGISTRY_TF = "modules/containerregistry/containerregistry.tf.jinja"
    COSMOS_DB_TF = "modules/cosmosdb/cosmosdb.tf.jinja"
    FUNCTION_APP_LINUX_TF = "modules/functionapp/functionapplinux.tf.jinja"
    FUNCTION_STORAGE_ACCOUNT_TF = "modules/storageaccount/functionstorage.tf.jinja"
    KEYVAULT_TF = "modules/keyvault/keyvault.tf.jinja"
    KEYVAULTSECRET_TF = "modules/keyvault/keyvaultsecret.tf.jinja"
    LOG_ANALYTICS_TF = "modules/loganalytics/loganalytics.tf.jinja"
    POSTGRESQL_TF = "modules/postgresqldb/postgresqldb.tf.jinja"
    REDIS_TF = "modules/redis/redis.tf.jinja"
    RESOURCE_GROUP_TF = "modules/resourcegroup/resourcegroup.tf.jinja"
    ROLE_TF = "modules/role/role.tf.jinja"
    SQL_DB_TF = "modules/sqldb/sqldb.tf.jinja"
    STORAGE_ACCOUNT_TF = "modules/storageaccount/storageaccount.tf.jinja"
    STORAGE_ACCOUNT_FIREWALL_TF = "modules/storageaccount/storageaccount.firewall.tf.jinja"
    STATIC_WEB_APP_TF = "modules/staticwebapp/staticwebapp.tf.jinja"
    SERVICE_BUS_TF = "modules/servicebus/servicebus.tf.jinja"
    SERVICE_BUS_NETWORK_TF = "modules/servicebus/servicebus.network.tf.jinja"
