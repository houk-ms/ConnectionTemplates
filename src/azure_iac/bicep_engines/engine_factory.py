from azure_iac.payloads.models.resource_type import ResourceType

from azure_iac.bicep_engines.modules.resource_engines.aisearch_engine import AISearchEngine
from azure_iac.bicep_engines.modules.resource_engines.aiservices_engine import AIServicesEngine
from azure_iac.bicep_engines.modules.resource_engines.applicationinsights_engine import ApplicationInsightsEngine
from azure_iac.bicep_engines.modules.resource_engines.appservice_engine import AppServiceEngine
from azure_iac.bicep_engines.modules.resource_engines.appservice_settings_engine import AppServiceSettingsEngine
from azure_iac.bicep_engines.modules.resource_engines.botservice_engine import BotServiceEngine
from azure_iac.bicep_engines.modules.resource_engines.containerapp_engine import ContainerAppEngine
from azure_iac.bicep_engines.modules.resource_engines.containerapp_settings_engine import ContainerAppSettingsEngine
from azure_iac.bicep_engines.modules.resource_engines.cosmosdb_engine import CosmosDbEngine
from azure_iac.bicep_engines.modules.resource_engines.functionapp_engine import FunctionAppEngine
from azure_iac.bicep_engines.modules.resource_engines.functionapp_settings_engine import FunctionAppSettingsEngine
from azure_iac.bicep_engines.modules.resource_engines.keyvault_engine import KeyVaultEngine
from azure_iac.bicep_engines.modules.resource_engines.mysqldb_engine import MySqlDbEngine
from azure_iac.bicep_engines.modules.resource_engines.openai_engine import OpenAIEngine
from azure_iac.bicep_engines.modules.resource_engines.postgresqldb_engine import PostgreSqlDbEngine
from azure_iac.bicep_engines.modules.resource_engines.redis_engine import RedisEngine
from azure_iac.bicep_engines.modules.resource_engines.sqldb_engine import SqlDbEngine
from azure_iac.bicep_engines.modules.resource_engines.servicebus_engine import ServiceBusEngine
from azure_iac.bicep_engines.modules.resource_engines.staticwebapp_engine import StaticWebAppEngine
from azure_iac.bicep_engines.modules.resource_engines.storageaccount_engine import StorageAccountEngine


RESOURCE_ENGINES = {
    ResourceType.AZURE_AI_SEARCH: AISearchEngine,
    ResourceType.AZURE_AI_SERVICES: AIServicesEngine,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ApplicationInsightsEngine,
    ResourceType.AZURE_APP_SERVICE: AppServiceEngine,
    ResourceType.AZURE_BOT_SERVICE: BotServiceEngine,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppEngine,
    ResourceType.AZURE_COSMOS_DB: CosmosDbEngine,
    ResourceType.AZURE_FUNCTION_APP: FunctionAppEngine,
    ResourceType.AZURE_KEYVAULT: KeyVaultEngine,
    ResourceType.AZURE_MYSQL_DB: MySqlDbEngine,
    ResourceType.AZURE_OPENAI: OpenAIEngine,
    ResourceType.AZURE_POSTGRESQL_DB: PostgreSqlDbEngine,
    ResourceType.AZURE_REDIS_CACHE: RedisEngine,
    ResourceType.AZURE_SERVICE_BUS: ServiceBusEngine,
    ResourceType.AZURE_SQL_DB: SqlDbEngine,
    ResourceType.AZURE_STATIC_WEB_APP: StaticWebAppEngine,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountEngine,
}

SETTING_ENGINES = {
    ResourceType.AZURE_APP_SERVICE: AppServiceSettingsEngine,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppSettingsEngine,
    ResourceType.AZURE_FUNCTION_APP: FunctionAppSettingsEngine,
}

def get_resource_engine_from_type(resource_type: ResourceType):
    return RESOURCE_ENGINES[resource_type]

def get_setting_engine_from_type(resource_type: ResourceType):
    return SETTING_ENGINES[resource_type]