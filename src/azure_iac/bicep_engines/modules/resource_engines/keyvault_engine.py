from typing import List

from azure_iac.helpers.connection_info import KeyVaultConnInfoHelper
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.keyvault import KeyVaultResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.bicep_engines.modules.store_resource_engine import StoreResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


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
        connInfoHelper = KeyVaultConnInfoHelper("" if binding.source.service is None else binding.source.service['language'],
                                                resource_endpoint='{}.outputs.endpoint'.format(self.module_name)
                                            )
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection)
        
        return self._get_app_settings(configs)
