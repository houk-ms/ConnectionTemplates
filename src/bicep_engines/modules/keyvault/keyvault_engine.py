from typing import List
from payloads.binding import Binding
from payloads.resources.keyvault import KeyVaultResource

from helpers.abbrevation import Abbreviation
from bicep_engines.models.appsetting import AppSetting, AppSettingType
from bicep_engines.models.template import Template
from bicep_engines.modules.target_resource_engine import TargetResourceEngine
from bicep_engines.modules.store_resource_engine import StoreResourceEngine

from helpers import string_helper


class KeyVaultEngine(TargetResourceEngine, StoreResourceEngine):

    def __init__(self, resource: KeyVaultResource) -> None:
        TargetResourceEngine.__init__(self,
                                      Template.KEYVAULT_BICEP.value,
                                      Template.KEYVAULT_MODULE.value)
        StoreResourceEngine.__init__(self,
                                        Template.KEYVAULT_BICEP.value,
                                        Template.KEYVAULT_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('keyVault', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('key-vault', self.resource.name)
        self.module_params_name = string_helper.format_camel('keyVault', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('key-vault', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.KEYVAULT.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('keyVault', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_KEYVAULT_RESOURCEENDPOINT'
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key,
                '{}.outputs.endpoint'.format(self.module_name)),
        ]
