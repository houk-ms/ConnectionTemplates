from payloads.models.resource_type import ResourceType

from engines.modules.appservice.appservice_engine import AppServiceEngine
from engines.modules.appservice.appservice_settings_engine import AppServiceSettingsEngine
from engines.modules.containerapp.containerapp_engine import ContainerAppEngine
from engines.modules.containerapp.containerapp_settings_engine import ContainerAppSettingsEngine
from engines.modules.keyvault.keyvault_engine import KeyVaultEngine
from engines.modules.storageaccount.storageaccount_engine import StorageAccountEngine


RESOURCE_ENGINES = {
    ResourceType.AZURE_APP_SERVICE: AppServiceEngine,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppEngine,
    ResourceType.AZURE_KEYVAULT: KeyVaultEngine,
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