from typing import List
from payloads.binding import Binding
from payloads.models.resource_type import ResourceType
from payloads.resources.storage_account import StorageAccountResource

from helpers.abbrevation import Abbreviation
from terraform_engines.models.template import Template
from terraform_engines.modules.target_resource_engine import TargetResourceEngine

from helpers import string_helper


class StorageAccountEngine(TargetResourceEngine):

    def __init__(self, resource: StorageAccountResource) -> None:
        super().__init__(Template.STORAGE_ACCOUNT_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake('sa', self.resource.name)
        
        # main.tf variables and outputs
        self.main_params = [
            ('storage_account_name', Abbreviation.STORAGE_ACCOUNT + string_helper.get_random_string(5)),
        ]
        self.main_outputs = [
            ('storage_account_id', 'azurerm_storage_account.storage_account.id')]


    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        # TODO: support multiple keys customizations
        return [
            ('AZURE_STORAGEBLOB_RESOURCEENDPOINT', '{}.outputs.blobEndpoint'.format(self.module_name)),
            ('AZURE_STORAGETABLE_RESOURCEENDPOINT', '{}.outputs.tableEndpoint'.format(self.module_name)),
            ('AZURE_STORAGEQUEUE_RESOURCEENDPOINT', '{}.outputs.queueEndpoint'.format(self.module_name)),
            ('AZURE_STORAGEFILE_RESOURCEENDPOINT', '{}.outputs.fileEndpoint'.format(self.module_name))
        ]
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_REDIS_CONNECTIONSTRING'

        if binding.source.type == ResourceType.AZURE_APP_SERVICE:
            return [
                (app_setting_key, '{}.outputs.appServiceSecretReference'.format(self.module_name))
            ]
        elif binding.source.type == ResourceType.AZURE_CONTAINER_APP:
            return [
                (app_setting_key, '{}.outputs.containerAppSecretReference'.format(self.module_name))
            ]