from enum import Enum


class ResourceType(str, Enum):
    AZURE_APP_SERVICE = "appservice"
    AZURE_APP_SERVICE_PLAN = "appserviceplan"
    AZURE_APPLICATION_INSIGHTS = "appinsights"
    AZURE_CONTAINER_APP = "containerapp"
    AZURE_CONTAINER_REGISTRY = "containerregistry"
    AZURE_COSMOS_DB = "cosmosdb"
    AZURE_FUNCTION_APP = "functionapp"
    AZURE_KEYVAULT = "keyvault"
    AZURE_POSTGRESQL_DB = "postgresqldb"
    AZURE_SPRING_APP = "springapp"
    AZURE_SQL_DB = "sqldb"
    AZURE_STORAGE_ACCOUNT = "storageaccount"
    

    def is_compute(self):
        return self in [
            ResourceType.AZURE_APP_SERVICE, 
            ResourceType.AZURE_CONTAINER_APP, 
            ResourceType.AZURE_FUNCTION_APP, 
            ResourceType.AZURE_SPRING_APP
        ]

