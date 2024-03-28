from payloads.models.resource_type import ResourceType

from terraform_engines.modules.appservice.appservice_engine import AppServiceEngine
from terraform_engines.modules.appservice.appservice_settings_engine import AppServiceSettingsEngine
from terraform_engines.modules.containerapp.containerapp_engine import ContainerAppEngine
from terraform_engines.modules.containerapp.containerapp_settings_engine import ContainerAppSettingsEngine
from terraform_engines.modules.applicationinsights.applicationinsights_engine import ApplicationInsightsEngine
from terraform_engines.modules.cosmosdb.cosmosdb_engine import CosmosDbEngine
from terraform_engines.modules.keyvault.keyvault_engine import KeyVaultEngine
from terraform_engines.modules.redis.redis_engine import RedisEngine
from terraform_engines.modules.sqldb.sqldb_engine import SqlDbEngine
from terraform_engines.modules.postgresqldb.postgresqldb_engine import PostgreSqlDbEngine
from terraform_engines.modules.storageaccount.storageaccount_engine import StorageAccountEngine



RESOURCE_ENGINES = {
    ResourceType.AZURE_APPLICATION_INSIGHTS: ApplicationInsightsEngine,
    ResourceType.AZURE_APP_SERVICE: AppServiceEngine,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppEngine,
    ResourceType.AZURE_COSMOS_DB: CosmosDbEngine,
    ResourceType.AZURE_KEYVAULT: KeyVaultEngine,
    ResourceType.AZURE_POSTGRESQL_DB: PostgreSqlDbEngine,
    ResourceType.AZURE_REDIS_CACHE: RedisEngine,
    ResourceType.AZURE_SQL_DB: SqlDbEngine,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountEngine
}

SETTING_ENGINES = {
    ResourceType.AZURE_APP_SERVICE: AppServiceSettingsEngine,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppSettingsEngine,
}

def get_resource_engine_from_type(resource_type: ResourceType):
    return RESOURCE_ENGINES[resource_type]

def get_setting_engine_from_type(resource_type: ResourceType):
    return SETTING_ENGINES[resource_type]