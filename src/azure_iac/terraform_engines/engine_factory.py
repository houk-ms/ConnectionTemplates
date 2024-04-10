from azure_iac.payloads.models.resource_type import ResourceType

from azure_iac.terraform_engines.modules.resource_engines.appservice_engine import AppServiceEngine
from azure_iac.terraform_engines.modules.resource_engines.containerapp_engine import ContainerAppEngine
from azure_iac.terraform_engines.modules.resource_engines.storageaccount_engine import StorageAccountEngine
from azure_iac.terraform_engines.modules.resource_engines.storageaccount_firewall_engine import StorageAccountFirewallEngine
from azure_iac.terraform_engines.modules.resource_engines.applicationinsights_engine import ApplicationInsightsEngine
from azure_iac.terraform_engines.modules.resource_engines.cosmosdb_engine import CosmosDbEngine
from azure_iac.terraform_engines.modules.resource_engines.keyvault_engine import KeyVaultEngine
from azure_iac.terraform_engines.modules.resource_engines.keyvaultsecret_engine import KeyVaultSecretEngine
from azure_iac.terraform_engines.modules.resource_engines.role_resource_engine import RoleResourceEngine


RESOURCE_ENGINES = {
	ResourceType.AZURE_APP_SERVICE: AppServiceEngine,
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

def get_key_vault_secret_engine():
	return KeyVaultSecretEngine
