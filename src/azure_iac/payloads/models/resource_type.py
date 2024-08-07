from enum import Enum

from azure_iac.payloads.models.connection_type import ConnectionType


class ResourceType(str, Enum):
    AZURE_AI_SEARCH = "azureaisearch"
    AZURE_AI_SERVICES = "azureaiservices"
    AZURE_APP_SERVICE = "azureappservice"
    AZURE_APPLICATION_INSIGHTS = "azureapplicationinsights"
    AZURE_BOT_SERVICE = "azurebotservice"
    AZURE_CONTAINER_APP = "azurecontainerapp"
    AZURE_COSMOS_DB = "azurecosmosdb"
    AZURE_FUNCTION_APP = "azurefunctions"
    AZURE_KEYVAULT = "azurekeyvault"
    AZURE_KUBERNETES_SERVICE = "azurekubernetesservice"
    AZURE_MYSQL_DB = "azuredatabaseformysql"
    AZURE_OPENAI = "azureopenai"
    AZURE_POSTGRESQL_DB = "azuredatabaseforpostgresql"
    AZURE_REDIS_CACHE = "azurecacheforredis"
    AZURE_SQL_DB = "azuresqldatabase"
    AZURE_STORAGE_ACCOUNT = "azurestorageaccount"
    AZURE_STATIC_WEB_APP = "azurestaticwebapp"
    AZURE_SERVICE_BUS = "azureservicebus"
    AZURE_USER_IDENTITY = "azureuseridentity"
    AZURE_WEBPUBSUB = "azurewebpubsub"


    def is_compute(self):
        return self in [
            ResourceType.AZURE_APP_SERVICE, 
            ResourceType.AZURE_CONTAINER_APP, 
            ResourceType.AZURE_FUNCTION_APP,
            ResourceType.AZURE_STATIC_WEB_APP,
            # ResourceType.AZURE_KUBERNETES_SERVICE,
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
            ResourceType.AZURE_MYSQL_DB,
            ResourceType.AZURE_POSTGRESQL_DB,
            ResourceType.AZURE_SQL_DB,
        ]

TargetDefaultConnectionType = {
    ResourceType.AZURE_AI_SEARCH: ConnectionType.SECRET,
    ResourceType.AZURE_AI_SERVICES: ConnectionType.SECRET,
    ResourceType.AZURE_APP_SERVICE: ConnectionType.HTTP,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ConnectionType.SECRET,
    ResourceType.AZURE_BOT_SERVICE: ConnectionType.BOTREGISTRATION,
    ResourceType.AZURE_CONTAINER_APP: ConnectionType.HTTP,
    ResourceType.AZURE_COSMOS_DB: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_FUNCTION_APP: ConnectionType.HTTP,
    ResourceType.AZURE_KEYVAULT: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_MYSQL_DB: ConnectionType.SECRET,
    ResourceType.AZURE_OPENAI: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_POSTGRESQL_DB: ConnectionType.SECRET,
    ResourceType.AZURE_REDIS_CACHE: ConnectionType.SECRET,
    ResourceType.AZURE_SQL_DB: ConnectionType.SECRET,
    ResourceType.AZURE_STORAGE_ACCOUNT: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_STATIC_WEB_APP: ConnectionType.HTTP,
    ResourceType.AZURE_SERVICE_BUS: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_OPENAI: ConnectionType.SYSTEMIDENTITY,
    ResourceType.AZURE_WEBPUBSUB: ConnectionType.SYSTEMIDENTITY,
}
