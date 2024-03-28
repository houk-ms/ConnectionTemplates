from enum import Enum


class ResourceType(str, Enum):
    AZURE_APP_SERVICE = "appservice"
    AZURE_APPLICATION_INSIGHTS = "appinsights"
    AZURE_CONTAINER_APP = "containerapp"
    AZURE_COSMOS_DB = "cosmos"
    AZURE_FUNCTION_APP = "functionapp"
    AZURE_KEYVAULT = "keyvault"
    AZURE_POSTGRESQL_DB = "postgresqldb"
    AZURE_REDIS_CACHE = "redis"
    AZURE_SQL_DB = "sqldb"
    AZURE_STORAGE_ACCOUNT = "storageaccount"


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
        ]