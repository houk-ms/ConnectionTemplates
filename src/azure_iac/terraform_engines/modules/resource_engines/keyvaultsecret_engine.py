from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType

from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation

class KeyVaultSecretEngine(BaseResourceEngine):

    def __init__(self, resource: TargetResourceEngine) -> None:
        super().__init__(Template.KEYVAULTSECRET_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.KEYVAULT_SECRET.value, self.resource.type, self.resource.name)
        self.module_params_name = (self.resource.type + self.resource.name or Abbreviation.KEYVAULT_SECRET.value) + '${var.resource_suffix}'
        
        self.module_params_key_vault_id = ''
        
        self.app_setting_key = ''
        self.module_params_value = ''

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('key', 'vault', 'secret', self.resource.type, self.resource.name, 'id'), self.get_secret_id())
        ]

    def get_secret_id(self):
        return 'azurerm_key_vault_secret.{}.id'.format(self.module_name)
    
    def get_key_vault_id(self, name):
        return 'azurerm_key_vault.{}.id'.format(string_helper.format_snake(Abbreviation.KEYVAULT.value, name))
    
    def set_key_vault_secret(self, binding: Binding, target_engine: TargetResourceEngine):
        app_setting_secret = target_engine.get_app_settings_secret(binding)[0]
        self.app_setting_key = app_setting_secret.name
        self.module_params_value = app_setting_secret.value
        self.module_params_key_vault_id = self.get_key_vault_id(binding.store.name)
    
    def get_app_settings(self) -> List[tuple]:
        return [
            AppSetting(AppSettingType.KeyVaultReference, self.app_setting_key, self.get_secret_id()) # format in source template
        ]

    def set_key_vault_secret(self, secret_name, secret_value, store_name) -> AppSetting:
        self.app_setting_key = secret_name
        self.module_params_value = secret_value
        self.module_params_key_vault_id = self.get_key_vault_id(store_name)
        return AppSetting(AppSettingType.KeyVaultReference, self.app_setting_key, self.get_secret_id()) # format in source template