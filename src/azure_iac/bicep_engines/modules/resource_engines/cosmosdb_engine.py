from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.cosmos_db import CosmosDBResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class CosmosDbEngine(TargetResourceEngine):

    def __init__(self, resource: CosmosDBResource) -> None:
        super().__init__(Template.COSMOS_DB_BICEP.value,
                         Template.COSMOS_DB_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('cosmosMongo', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('cosmos-mongo', self.resource.name)
        self.module_params_name = string_helper.format_camel('cosmosMongo', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('cosmos-mongo', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.COSMOS_DB.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('cosmosMongo', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_COSMOS_RESOURCEENDPOINT'
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key, 
                '{}.outputs.endpoint'.format(self.module_name)),
        ]
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_COSMOS_CONNECTIONSTRING'

        return [
            AppSetting(AppSettingType.KeyVaultReference, app_setting_key,
                '{}.outputs.keyVaultSecretUri'.format(self.module_name))
        ]