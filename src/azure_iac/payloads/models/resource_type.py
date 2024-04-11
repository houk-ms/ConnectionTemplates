from enum import Enum

from azure_iac.payloads.models.connection_type import ConnectionType


class ResourceType(str, Enum):
    AZURE_APP_SERVICE = "azureappservice"
    AZURE_APPLICATION_INSIGHTS = "azureapplicationinsights"
    AZURE_BOT_SERVICE = "azurebotservice"
    AZURE_CONTAINER_APP = "azurecontainerapp"
    AZURE_COSMOS_DB = "azurecosmosdb"
    AZURE_FUNCTION_APP = "azurefunctions"
    AZURE_KEYVAULT = "azurekeyvault"
    AZURE_MYSQL_DB = "azuremysqldatabase"
    AZURE_POSTGRESQL_DB = "azuredatabaseforpostgresql"
    AZURE_REDIS_CACHE = "azurecacheforredis"
    AZURE_SQL_DB = "azuresqldatabase"
    AZURE_STORAGE_ACCOUNT = "azurestorageaccount"
    AZURE_STATIC_WEB_APP = "azurestaticwebapp"
    AZURE_SERVICE_BUS = "azureservicebus"


    def is_compute(self):
        return self in [
            ResourceType.AZURE_APP_SERVICE, 
            ResourceType.AZURE_CONTAINER_APP, 
            ResourceType.AZURE_FUNCTION_APP, 
        ]

    # targets that supports TF firewall rules
    def is_target_with_firewall(self):
        return self in [
            ResourceType.AZURE_COSMOS_DB, 
            ResourceType.AZURE_POSTGRESQL_DB, 
            ResourceType.AZURE_REDIS_CACHE, 
            ResourceType.AZURE_SQL_DB, 
            ResourceType.AZURE_STORAGE_ACCOUNT, 
            ResourceType.AZURE_MYSQL_DB,
            ResourceType.AZURE_SERVICE_BUS,
        ]

TargetDefaultConnectionType = {
    ResourceType.AZURE_APP_SERVICE: ConnectionType.HTTP,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ConnectionType.SECRET,
    ResourceType.AZURE_BOT_SERVICE: ConnectionType.BOTREGISTRATION,
    ResourceType.AZURE_CONTAINER_APP: ConnectionType.HTTP,
    ResourceType.AZURE_COSMOS_DB: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_FUNCTION_APP: ConnectionType.HTTP,
    ResourceType.AZURE_KEYVAULT: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_MYSQL_DB: ConnectionType.SECRET,
    ResourceType.AZURE_POSTGRESQL_DB: ConnectionType.SECRET,
    ResourceType.AZURE_REDIS_CACHE: ConnectionType.SECRET,
    ResourceType.AZURE_SQL_DB: ConnectionType.SECRET,
    ResourceType.AZURE_STORAGE_ACCOUNT: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_STATIC_WEB_APP: ConnectionType.HTTP,
    ResourceType.AZURE_SERVICE_BUS: ConnectionType.SECRET,
}
