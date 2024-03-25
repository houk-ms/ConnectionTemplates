from typing import List
from payloads.models.resource_type import ResourceType
from payloads.resources.storage_account import StorageAccountResource

from engines.models.abbrevation import Abbreviation
from engines.models.template import Template
from engines.modules.target_resource_engine import TargetResourceEngine

from helpers import string_helper


class StorageAccountEngine(TargetResourceEngine):

    def __init__(self, resource: StorageAccountResource) -> None:
        super().__init__(Template.STORAGE_ACCOUNT_BICEP.value,
                         Template.STORAGE_ACCOUNT_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('storageAccount', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('storage-account', self.resource.name)
        self.module_params_name = string_helper.format_camel('storageAccount', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('storage-account', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.STORAGE_ACCOUNT.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('storageAccount', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by identity connection
    def get_app_settings_identity(self) -> List[tuple]:
        return [
            ('AZURE_STORAGE_BLOB_ENDPOINT', '{}.outputs.blobEndpoint'.format(self.module_name)),
            ('AZURE_STORAGE_TABLE_ENDPOINT', '{}.outputs.tableEndpoint'.format(self.module_name)),
            ('AZURE_STORAGE_QUEUE_ENDPOINT', '{}.outputs.queueEndpoint'.format(self.module_name)),
            ('AZURE_STORAGE_FILE_ENDPOINT', '{}.outputs.fileEndpoint'.format(self.module_name))
        ]
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, compute: ResourceType) -> List[tuple]:
        if compute == ResourceType.AZURE_APP_SERVICE:
            return [
                ('AZURE_STORAGE_CONNECTION_STRING', '{}.outputs.appServiceSecretReference'.format(self.module_name))
            ]
        elif compute == ResourceType.AZURE_CONTAINER_APP:
            return [
                ('AZURE_STORAGE_CONNECTION_STRING', '{}.outputs.containerAppSecretReference'.format(self.module_name))
            ]