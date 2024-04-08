from enum import Enum


class ResourceType(str, Enum):
    AZURE_APP_SERVICE = "azureappservice"
    AZURE_APPLICATION_INSIGHTS = "azureapplicationinsights"
    AZURE_CONTAINER_APP = "azurecontainerapp"
    AZURE_COSMOS_DB = "azurecosmosdb"
    AZURE_FUNCTION_APP = "azurefunctions"
    AZURE_KEYVAULT = "azurekeyvault"
    AZURE_POSTGRESQL_DB = "azuredatabaseforpostgresql"
    AZURE_REDIS_CACHE = "azurecacheforredis"
    AZURE_SQL_DB = "azuresqldatabase"
    AZURE_STORAGE_ACCOUNT = "azurestorageaccount"
    AZURE_MYSQL_DB = "azuremysqldatabase"


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
        ]