from payloads.models.resource_type import ResourceType


from terraform_engines.modules.containerapp.containerapp_engine import ContainerAppEngine
from terraform_engines.modules.storageaccount.storageaccount_engine import StorageAccountEngine
from terraform_engines.modules.storageaccount.storageaccount_firewall_engine import StorageAccountFirewallEngine
from terraform_engines.modules.applicationinsights.applicationinsights_engine import ApplicationInsightsEngine
from terraform_engines.modules.cosmosdb.cosmosdb_engine import CosmosDbEngine
from terraform_engines.modules.keyvault.keyvault_engine import KeyVaultEngine
from terraform_engines.modules.role.role_resource_engine import RoleResourceEngine


RESOURCE_ENGINES = {
    ResourceType.AZURE_CONTAINER_APP: ContainerAppEngine,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountEngine,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ApplicationInsightsEngine,
    ResourceType.AZURE_COSMOS_DB: CosmosDbEngine,
    ResourceType.AZURE_KEYVAULT: KeyVaultEngine,
}

FIREWALL_ENGINES = {
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountFirewallEngine,
}

def get_resource_engine_from_type(resource_type: ResourceType):
    return RESOURCE_ENGINES[resource_type]

def get_firewall_engine_from_type(resource_type: ResourceType):
    return FIREWALL_ENGINES.get(resource_type)

def get_role_engine():
    return RoleResourceEngine
